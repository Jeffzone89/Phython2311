"""Stage 1 PoC: 네이버쇼핑 검색결과 페이지를 직접 조회해 실제 구조를 확인한다.

    python3 price-monitor/poc/poc_inspect_response.py

API 키가 필요 없다(공식 API가 막혀 있어 페이지를 직접 파싱하는 방식으로 전환했다,
README의 Stage 0 기록 참고). naver_search_client.py의 __NEXT_DATA__ 파싱 가정이
실제와 다르면 여기서 SearchPageError가 발생한다 - 그러면 poc_catalog_page.py를
검색결과 URL로 실행해 원본 HTML을 저장하고 실제 구조를 직접 확인할 것.

각 항목의 link가 '/catalog/'를 포함하는지(그룹상품 여부), mallName이
"힐러문"으로 정확히 노출되는지를 직접 눈으로 확인하기 위한 스크립트다.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import KEYWORD  # noqa: E402
import naver_search_client  # noqa: E402


def main():
    items = naver_search_client.search_shopping(query=KEYWORD)
    print(f"총 {len(items)}건 조회\n")
    for item in items:
        is_catalog = "/catalog/" in (item.get("link") or "")
        print(json.dumps(item, ensure_ascii=False, indent=2))
        print(f"  -> catalog 여부(link 기준): {is_catalog}\n")


if __name__ == "__main__":
    main()
