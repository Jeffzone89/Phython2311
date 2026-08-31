#!/usr/bin/env python3
"""상세페이지 HTML을 상품등록용 이미지 한 장으로 렌더링합니다.

  python3 tools/render.py

가로 860px(네이버 스마트스토어 권장 폭) 기준입니다.
2배 해상도로 캡처한 뒤 860px로 축소해 텍스트를 선명하게 만듭니다.
"""
import asyncio, pathlib
from PIL import Image
from playwright.async_api import async_playwright

ROOT   = pathlib.Path(__file__).resolve().parent.parent
SRC    = ROOT / "cholesta-detail.html"
OUT    = ROOT / "images" / "cholesta-detail.png"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

WIDTH = 860      # 최종 이미지 가로 폭(px)
SCALE = 2        # 캡처 배율


async def main():
    OUT.parent.mkdir(exist_ok=True)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(executable_path=CHROME)
        page = await browser.new_page(
            viewport={"width": WIDTH, "height": 1200}, device_scale_factor=SCALE
        )
        await page.goto(SRC.as_uri())
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(OUT), full_page=True)
        await browser.close()

    im = Image.open(OUT).convert("RGB")
    im = im.resize((WIDTH, round(im.height / SCALE)), Image.LANCZOS)
    im.save(OUT, optimize=True)
    print(f"{OUT.name}  {im.width} x {im.height}  "
          f"{OUT.stat().st_size / 1024:.0f}KB")


if __name__ == "__main__":
    asyncio.run(main())
