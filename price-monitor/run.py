import argparse
import datetime

import matcher
import naver_api_client
import state_store
import telegram_notifier
from config import KEYWORD


def decide_alerts(group_key, prev, result, first_run):
    alerts = []

    if result.needs_admin_check:
        alerts.append(f"🔧 [점검 필요] {group_key}\n{result.note}")
        return alerts

    if not result.owner_found:
        if first_run or prev.get("owner_found", True):
            alerts.append(f"❗ [노출 확인 필요] {group_key}\n힐러문 상품이 검색결과에서 확인되지 않습니다.")
        return alerts

    if first_run:
        return alerts

    was_cheapest = prev.get("is_owner_cheapest")
    if was_cheapest and not result.is_owner_cheapest:
        diff = result.owner_price - result.cheapest_price
        alerts.append(
            f"⚠️ [{KEYWORD}] 최저가 이탈 ({group_key})\n"
            f"현재 최저가: {result.cheapest_mall} {result.cheapest_price:,}원\n"
            f"힐러문: {result.owner_price:,}원 ({diff:,}원 차이)"
        )
    elif was_cheapest is False and result.is_owner_cheapest:
        alerts.append(f"✅ [{KEYWORD}] 최저가 회복 ({group_key})\n힐러문: {result.owner_price:,}원")

    return alerts


def result_to_state(result):
    return {
        "owner_found": result.owner_found,
        "is_owner_cheapest": result.is_owner_cheapest,
        "owner_price": result.owner_price,
        "cheapest_price": result.cheapest_price,
        "cheapest_mall": result.cheapest_mall,
        "updated_at": datetime.datetime.now().isoformat(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="알림 발송/상태 저장 없이 콘솔에만 출력")
    parser.add_argument("--test-alert", action="store_true", help="텔레그램 배선 확인용 테스트 메시지 1건만 발송")
    args = parser.parse_args()

    if args.test_alert:
        telegram_notifier.send_message("✅ price-monitor 테스트 알림입니다.")
        print("테스트 알림 발송 완료")
        return

    items = naver_api_client.search_shopping()
    groups = matcher.build_groups(items)

    prev_state = state_store.load_state()
    new_state = {}
    all_alerts = []

    for group_key, result in groups.items():
        prev = prev_state.get(group_key, {})
        first_run = group_key not in prev_state
        alerts = decide_alerts(group_key, prev, result, first_run)
        all_alerts.extend(alerts)
        new_state[group_key] = result_to_state(result)

    for text in all_alerts:
        print(text)
        if not args.dry_run:
            telegram_notifier.send_message(text)

    if args.dry_run:
        print("(dry-run: 상태 저장 안 함)")
    else:
        state_store.save_state(new_state)


if __name__ == "__main__":
    main()
