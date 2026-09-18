import re
import warnings
from dataclasses import dataclass
from typing import Optional

import catalog_fetcher
from config import OWNER_MALL_NAME, OWNER_PRODUCT_ID, OWNER_STORE_SLUG, PRODUCT_VARIANTS
from naver_search_client import product_kind

CATALOG_LINK_PATTERN = re.compile(r"/catalog/(\d+)")
# 공식 문서 productType 표 기준: 상품종류 1 = "가격비교 상품"(그룹 대표 항목).
CATALOG_PRODUCT_KIND = 1


@dataclass
class GroupResult:
    group_key: str
    owner_found: bool
    needs_admin_check: bool = False
    is_owner_cheapest: Optional[bool] = None
    owner_price: Optional[int] = None
    cheapest_price: Optional[int] = None
    cheapest_mall: Optional[str] = None
    note: str = ""


def build_groups(items):
    """검색결과 items를 그룹(카탈로그 또는 수동 지정 variant)으로 묶어 평가한다."""
    groups = {}

    catalog_ids = set()
    for item in items:
        m = CATALOG_LINK_PATTERN.search(item.get("link") or "")
        if m:
            catalog_ids.add(m.group(1))
            if product_kind(item.get("productType")) != CATALOG_PRODUCT_KIND:
                warnings.warn(
                    f"link는 /catalog/ 패턴인데 productType={item.get('productType')}로 "
                    f"'가격비교 상품'이 아님 (productId={item.get('productId')}) - 교차검증 실패, 확인 필요"
                )

    for catalog_id in catalog_ids:
        group_key = f"catalog:{catalog_id}"
        groups[group_key] = _evaluate_catalog_group(group_key, catalog_id)

    non_catalog_items = [item for item in items if not CATALOG_LINK_PATTERN.search(item.get("link") or "")]
    for variant in PRODUCT_VARIANTS:
        matched = [item for item in non_catalog_items if _title_matches(item["title"], variant)]
        if not matched:
            continue
        group_key = f"individual:{variant['key']}"
        sellers = [
            {"mallName": i["mallName"], "price": i["lprice"], "productId": i["productId"], "link": i["link"]}
            for i in matched
        ]
        groups[group_key] = _evaluate_owner_status(group_key, sellers)

    return groups


def _title_matches(title, variant):
    if not all(kw in title for kw in variant.get("match_keywords", [])):
        return False
    if any(kw in title for kw in variant.get("exclude_keywords", [])):
        return False
    return True


def _evaluate_catalog_group(group_key, catalog_id):
    try:
        sellers = catalog_fetcher.fetch_sellers(catalog_id)
    except (catalog_fetcher.ParserDriftError, NotImplementedError) as exc:
        return GroupResult(
            group_key=group_key,
            owner_found=False,
            needs_admin_check=True,
            note=f"카탈로그 판매처 조회 실패: {exc}",
        )
    return _evaluate_owner_status(group_key, sellers)


def _identify_owner(sellers):
    by_id = [s for s in sellers if OWNER_PRODUCT_ID and s.get("productId") == OWNER_PRODUCT_ID]
    by_name = [
        s
        for s in sellers
        if s.get("mallName") == OWNER_MALL_NAME
        and (not OWNER_STORE_SLUG or OWNER_STORE_SLUG in (s.get("link") or ""))
    ]
    if by_id and by_name and by_id[0].get("productId") != by_name[0].get("productId"):
        return None, "ambiguous"
    match = by_id or by_name
    if match:
        return match[0], "ok"
    return None, "not_found"


def _evaluate_owner_status(group_key, sellers):
    if not sellers:
        return GroupResult(group_key=group_key, owner_found=False, note="판매처 목록이 비어있음")

    owner, status = _identify_owner(sellers)
    if status == "ambiguous":
        return GroupResult(
            group_key=group_key,
            owner_found=False,
            needs_admin_check=True,
            note="productId 매칭과 mallName 매칭 결과가 서로 다름 - 수동 확인 필요",
        )
    if owner is None or owner.get("price") is None:
        return GroupResult(group_key=group_key, owner_found=False)

    priced = [s for s in sellers if s.get("price") is not None]
    cheapest = min(priced, key=lambda s: s["price"])
    return GroupResult(
        group_key=group_key,
        owner_found=True,
        is_owner_cheapest=owner["price"] <= cheapest["price"],
        owner_price=owner["price"],
        cheapest_price=cheapest["price"],
        cheapest_mall=cheapest["mallName"],
    )
