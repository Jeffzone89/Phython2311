# 콜레스타 상세페이지

건강기능식품 "콜레스타" 상품등록용 상세페이지입니다.

## 파일

| 경로 | 설명 |
|---|---|
| `cholesta-detail.html` | 상세페이지 원본 (단일 HTML, 외부 의존성 없음) |
| `tools/render.py` | HTML → 상품등록용 PNG 렌더링 스크립트 |
| `images/` | 렌더링된 결과 이미지 |

## 이미지

가로 **860px** (네이버 스마트스토어 권장 폭) 기준입니다.

- `cholesta-detail-full.png` — 전체 1장 (860 × 3144)
- `cholesta-01_header.png` ~ `cholesta-05_product.png` — 섹션별 분할본

분할본은 위에서부터 순서대로 이어붙이면 전체본과 동일합니다.

## 색상 변경

`cholesta-detail.html` 상단의 `:root` 블록에 색상 토큰이 모여 있습니다.
이 값만 바꾸면 페이지 전체 톤이 바뀝니다.

```css
:root{
  --green:#1f4438;      /* 메인 딥그린 */
  --gold:#b08d57;       /* 포인트 골드 */
  --ivory:#f7f4ee;      /* 배경 아이보리 */
  ...
}
```

## 이미지 다시 만들기

```bash
pip install playwright pillow
python3 tools/render.py
```

한글은 Pretendard로 렌더링됩니다. 폰트가 없으면 `npm pack pretendard` 로 받아
`~/.fonts/` 에 넣고 `fc-cache -f` 를 실행하세요.

## 주의

표기 문구(기능성 정보, 영양성분, 원료명, 주의사항)는 제품 표시사항을 그대로
옮긴 것입니다. 임의로 수정하면 표시·광고 규정에 어긋날 수 있습니다.
