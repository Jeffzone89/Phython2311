#!/usr/bin/env python3
"""상세페이지 HTML을 상품등록용 이미지로 렌더링합니다.

  python3 tools/render.py

- 가로 860px (네이버 스마트스토어 권장 폭) 기준으로 렌더링합니다.
- 2배 해상도로 캡처한 뒤 860px로 축소해 텍스트를 선명하게 만듭니다.
- 전체 1장과 섹션별 분할본을 images/ 아래에 저장합니다.
"""
import asyncio, pathlib
from PIL import Image
from playwright.async_api import async_playwright

ROOT   = pathlib.Path(__file__).resolve().parent.parent
SRC    = ROOT / "cholesta-detail.html"
IMAGES = ROOT / "images"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

WIDTH  = 860      # 최종 이미지 가로 폭(px)
SCALE  = 2        # 캡처 배율

# (파일명, 시작 기준 셀렉터) — 각 구간은 다음 항목의 시작점까지
CUTS = [
    ("01_header",      None),
    ("02_function",    "section:nth-of-type(1)"),
    ("03_nutrition",   "section:nth-of-type(2)"),
    ("04_ingredients", "section.raw"),
    ("05_product",     "section:nth-of-type(4)"),
]


async def main():
    IMAGES.mkdir(exist_ok=True)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(executable_path=CHROME)
        page = await browser.new_page(
            viewport={"width": WIDTH, "height": 1200}, device_scale_factor=SCALE
        )
        await page.goto(SRC.as_uri())
        await page.wait_for_timeout(300)

        offsets = [0]
        for _, sel in CUTS[1:]:
            offsets.append(await page.evaluate(
                "s => Math.round(document.querySelector(s)"
                ".getBoundingClientRect().top + window.scrollY)", sel))

        full_path = IMAGES / "cholesta-detail-full.png"
        await page.screenshot(path=str(full_path), full_page=True)
        await browser.close()

    full = Image.open(full_path).convert("RGB")
    target_h = round(full.height / SCALE)
    full = full.resize((WIDTH, target_h), Image.LANCZOS)
    full.save(full_path, optimize=True)
    print(f"{full_path.name:<32} {full.width} x {full.height}")

    bounds = offsets + [target_h]
    for (name, _), top, bottom in zip(CUTS, bounds, bounds[1:]):
        part = full.crop((0, top, WIDTH, bottom))
        out = IMAGES / f"cholesta-{name}.png"
        part.save(out, optimize=True)
        print(f"{out.name:<32} {part.width} x {part.height}")


if __name__ == "__main__":
    asyncio.run(main())
