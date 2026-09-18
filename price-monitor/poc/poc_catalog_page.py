"""Stage 1 PoC: 카탈로그 상품 페이지의 원본 구조를 확인한다.

    python3 price-monitor/poc/poc_catalog_page.py <카탈로그 URL>

판매처별 가격 목록이 정적 HTML에 있는지, JS 렌더링이 필요한 SPA인지
직접 확인하기 위한 스크립트다. 저장된 HTML에서 판매처명/가격이 텍스트로
보이면 정적 requests 파싱으로 충분하고, 안 보이면 catalog_fetcher.py에서
tools/render.py와 같은 Playwright 렌더링이 필요하다.
"""
import sys

import requests

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)


def main():
    if len(sys.argv) < 2:
        print("사용법: python3 poc_catalog_page.py <카탈로그 URL>")
        sys.exit(1)

    url = sys.argv[1]
    resp = requests.get(url, headers={"User-Agent": UA}, timeout=10)
    print(f"status: {resp.status_code}, 길이: {len(resp.text)}자")

    out_path = "poc_catalog_page_output.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(resp.text)
    print(f"HTML을 {out_path}에 저장했습니다. 에디터로 열어 판매처명/가격 텍스트가 보이는지 확인하세요.")


if __name__ == "__main__":
    main()
