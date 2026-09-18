"""일회성 테스트: r.jina.ai 같은 외부 리더 프록시를 통해 네이버쇼핑 검색결과를
가져올 수 있는지 확인한다. GitHub Actions IP가 네이버에 직접 차단당해서(418),
다른 네트워크 경로로 우회 가능한지 빠르게 검증하기 위한 일회성 스크립트다.
"""
import sys

import requests

TARGET = "https://search.shopping.naver.com/search/all?query=%EC%BD%9C%EB%A0%88%EC%8A%A4%ED%83%80"

CANDIDATES = {
    "jina_reader": f"https://r.jina.ai/{TARGET}",
}


def main():
    for name, url in CANDIDATES.items():
        print(f"=== {name} ===")
        try:
            resp = requests.get(url, timeout=20)
            print(f"status: {resp.status_code}, 길이: {len(resp.text)}자")
            snippet = resp.text[:2000]
            print(snippet)
            has_cholesta = "콜레스타" in resp.text
            print(f"\n'콜레스타' 텍스트 포함 여부: {has_cholesta}")
        except Exception as exc:
            print(f"실패: {exc}")
        print()


if __name__ == "__main__":
    main()
    sys.exit(0)
