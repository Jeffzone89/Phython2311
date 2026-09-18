"""일회성 테스트 스크립트 (용도는 그때그때 바뀜).

현재: apicenter.commerce.naver.com의 API 문서 페이지를 직접 조회해
"카탈로그 조회" 등 커머스API가 판매처별 가격 정보를 주는지 확인한다.
문서 페이지라 쇼핑 검색결과 페이지와 달리 차단 대상이 아닐 가능성이 높다.
"""
import requests

DOCS_URL = "https://apicenter.commerce.naver.com/docs/commerce-api/current/get-model-list-product"

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    ),
}


def main():
    print(f"=== {DOCS_URL} ===")
    try:
        resp = requests.get(DOCS_URL, headers=_HEADERS, timeout=20)
        print(f"status: {resp.status_code}, 길이: {len(resp.text)}자\n")
        print(resp.text)
    except Exception as exc:
        print(f"실패: {exc}")


if __name__ == "__main__":
    main()
