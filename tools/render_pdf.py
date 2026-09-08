#!/usr/bin/env python3
"""제안서 HTML을 A4 PDF로 뽑습니다.

  python3 tools/render_pdf.py

proposal/cholesta-proposal.html 상단 DATA 블록을 고친 뒤 다시 실행하면
같은 자리에 PDF가 새로 만들어집니다.
"""
import asyncio
import pathlib
import sys

from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "proposal" / "cholesta-proposal.html"
OUT = ROOT / "proposal" / "cholesta-proposal.pdf"

# 컨테이너에 설치된 Chromium. 다른 PC에서는 None으로 두면 playwright가 알아서 찾습니다.
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"


async def main() -> None:
    if not SRC.exists():
        sys.exit(f"원본을 찾을 수 없습니다: {SRC}")

    chrome = CHROME if pathlib.Path(CHROME).exists() else None

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(executable_path=chrome)
        page = await browser.new_page()
        await page.goto(SRC.as_uri())
        await page.wait_for_timeout(400)  # 폰트 로딩 대기
        await page.pdf(
            path=str(OUT),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True,
        )
        await browser.close()

    print(f"{OUT.relative_to(ROOT)}  {OUT.stat().st_size / 1024:.0f}KB")


if __name__ == "__main__":
    asyncio.run(main())
