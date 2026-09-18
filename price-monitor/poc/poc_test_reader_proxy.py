"""일회성 테스트 스크립트 (용도는 그때그때 바뀜).

현재: blackpoint.codes/tracking 페이지 내용을 확인한다 (사용자가 공유).
"""
from playwright.sync_api import sync_playwright

URL = "https://blackpoint.codes/tracking"


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(locale="ko-KR")
        resp = page.goto(URL, timeout=20000, wait_until="networkidle")
        print(f"status: {resp.status if resp else None}")
        text = page.inner_text("body")
        print(f"본문 길이: {len(text)}자\n")
        print(text)
        browser.close()


if __name__ == "__main__":
    main()
