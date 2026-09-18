import re
import time

import requests

from config import DISPLAY, KEYWORD, NAVER_API_URL, NAVER_CLIENT_ID, NAVER_CLIENT_SECRET, SORT

_TAG_RE = re.compile(r"<.*?>")


class NaverApiError(Exception):
    pass


def search_shopping(query=KEYWORD, display=DISPLAY, sort=SORT, start=1, max_retries=2):
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    params = {"query": query, "display": display, "sort": sort, "start": start}

    attempt = 0
    while True:
        resp = requests.get(NAVER_API_URL, headers=headers, params=params, timeout=10)
        if resp.status_code == 200:
            break
        if resp.status_code in (429, 500, 502, 503, 504) and attempt < max_retries:
            time.sleep(2 ** attempt)
            attempt += 1
            continue
        raise NaverApiError(f"Naver API 요청 실패: {resp.status_code} {resp.text}")

    data = resp.json()
    return [_normalize(item) for item in data.get("items", [])]


def _normalize(item):
    lprice = item.get("lprice")
    return {
        "productId": item.get("productId"),
        "productType": item.get("productType"),
        "mallName": item.get("mallName"),
        "lprice": int(lprice) if lprice else None,
        "link": item.get("link"),
        "title": _TAG_RE.sub("", item.get("title") or ""),
    }
