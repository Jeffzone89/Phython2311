"""Stage 1 PoC: 네이버 오픈API 쇼핑검색 원시 응답을 확인한다.

실행 전 환경변수 NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 설정 필요.

    export NAVER_CLIENT_ID=...
    export NAVER_CLIENT_SECRET=...
    python3 price-monitor/poc/poc_inspect_response.py

각 항목의 link가 '/catalog/'를 포함하는지(그룹상품 여부), mallName이
"힐러문"으로 정확히 노출되는지를 직접 눈으로 확인하기 위한 스크립트다.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import KEYWORD  # noqa: E402
import naver_api_client  # noqa: E402


def main():
    items = naver_api_client.search_shopping(query=KEYWORD)
    print(f"총 {len(items)}건 조회\n")
    for item in items:
        is_catalog = "/catalog/" in (item.get("link") or "")
        print(json.dumps(item, ensure_ascii=False, indent=2))
        print(f"  -> catalog 여부(link 기준): {is_catalog}\n")


if __name__ == "__main__":
    main()
