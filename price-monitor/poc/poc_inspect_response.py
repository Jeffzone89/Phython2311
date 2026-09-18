"""Stage 1 PoC: 네이버쇼핑 검색결과 페이지를 직접 조회해 실제 구조를 확인한다.

    python3 price-monitor/poc/poc_inspect_response.py

API 키가 필요 없다(공식 API가 막혀 있어 페이지를 직접 파싱하는 방식으로 전환했다,
README의 Stage 0 기록 참고). 원본 HTML은 파싱 성공 여부와 무관하게 항상
poc/raw_page_dump.html로 저장한다 - naver_search_client.py의 __NEXT_DATA__ 파싱
가정이 실제와 다르면(SearchPageError), 이 파일을 열어 실제 구조를 직접 확인하고
_find_item_list()/_normalize()를 다시 구현할 것.

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
    html = naver_search_client.fetch_html(query=KEYWORD)
    os.makedirs(os.path.dirname(naver_search_client.RAW_DUMP_PATH), exist_ok=True)
    with open(naver_search_client.RAW_DUMP_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"원본 HTML을 {naver_search_client.RAW_DUMP_PATH}에 저장했습니다 ({len(html)}자)\n")

    match = naver_search_client._NEXT_DATA_RE.search(html)
    print(f"__NEXT_DATA__ 발견 여부: {bool(match)}\n")

    items = naver_search_client.parse_html(html)
    print(f"총 {len(items)}건 조회\n")
    for item in items:
        is_catalog = "/catalog/" in (item.get("link") or "")
        print(json.dumps(item, ensure_ascii=False, indent=2))
        print(f"  -> catalog 여부(link 기준): {is_catalog}\n")


if __name__ == "__main__":
    main()
