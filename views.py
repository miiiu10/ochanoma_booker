import json
from typing import Any, Optional, List


def view_home(user_id: str) -> dict[str, Any]:
    google_calendar_url = "https://calendar.google.com/calendar/u/0?cid=Y19uNzNwbGVzZWtxYXRzanU2aDFjcTFibjJhc0Bncm91cC5jYWxlbmRhci5nb29nbGUuY29t"  # noqa: E501
    scrap_box_url = (
        "https://scrapbox.io/iiclab/OchanomaBooker%E3%81%AE%E4%BD%BF%E3%81%84%E6%96%B9"
    )
    view = {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "お茶の間予約システム :tea:"},
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"<@{user_id}>さん、ここでお茶の間の予約をしてみましょう :tada:\n"
                        f"使い方は<{scrap_box_url}|*Scrapbox*>を参考にしてください :green_book:\n"
                    ),
                },
            },
            {"type": "divider"},
            {
                "type": "input",
                "element": {
                    "type": "datepicker",
                    "placeholder": {"type": "plain_text", "text": "Select a date"},
                    "action_id": "datepick",
                },
                "label": {"type": "plain_text", "text": ":calendar: 日付", "emoji": True},
                "block_id": "dateblock",
            },
            {
                "type": "input",
                "element": {
                    "type": "timepicker",
                    "placeholder": {"type": "plain_text", "text": "Select start time"},
                    "action_id": "timepick",
                },
                "label": {
                    "type": "plain_text",
                    "text": ":alarm_clock: 開始時間",
                    "emoji": True,
                },
                "block_id": "start_time_block",
            },
            {
                "type": "input",
                "element": {
                    "type": "timepicker",
                    "placeholder": {"type": "plain_text", "text": "Select end time"},
                    "action_id": "timepick",
                },
                "label": {
                    "type": "plain_text",
                    "text": ":alarm_clock: 終了時間",
                    "emoji": True,
                },
                "block_id": "end_time_block",
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "※ 分刻みの場合は直接入力してください :keyboard:",
                },
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "placeholder": {"type": "plain_text", "text": "Write description"},
                    "action_id": "description",
                },
                "label": {
                    "type": "plain_text",
                    "text": ":mag: 詳細 (任意入力)",
                    "emoji": True,
                },
                "block_id": "textblock",
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "style": "primary",
                        "text": {"type": "plain_text", "text": "追加"},
                        "value": "home_add",
                        "action_id": "add_home",
                    }
                ],
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": " ",
                },
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": " ",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":busts_in_silhouette: *みんなの予約*",
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "確認"},
                    "value": "home_check",
                    "action_id": "check_home",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":bust_in_silhouette: *自分の予約*",
                },
                "accessory": {
                    "type": "button",
                    "style": "danger",
                    "text": {"type": "plain_text", "text": "確認・削除"},
                    "value": "home_delete",
                    "action_id": "delete_home",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"予約状況は<{google_calendar_url}|*Google Calendar*>からも確認できます :eyes:\n",
                },
            },
        ],
    }
    return view


def view_schedule(text) -> dict[str, Any]:
    view = {
        "type": "modal",
        "callback_id": "view_before",
        "title": {"type": "plain_text", "text": "Schedule"},
        "blocks": [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": ("checking schedule")},
            },
            {"type": "divider"},
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
        ],
    }
    return view


def view_add_reminder(user_id: str) -> dict[str, Any]:
    view = {
        "type": "modal",
        "callback_id": "view_reminder_add",
        "title": {"type": "plain_text", "text": "リマインダーの追加"},
        "submit": {"type": "plain_text", "text": "確定"},
        "close": {"type": "plain_text", "text": "キャンセル"},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<@{user_id}>さん、リマインダーを作成してみましょう！\n日付と時間を選択して *確定* ボタンを押してください。",
                },
            },
            {"type": "divider"},
            {
                "type": "input",
                "element": {
                    "type": "datepicker",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date",
                        "emoji": True,
                    },
                    "action_id": "datepicker-action",
                },
                "label": {"type": "plain_text", "text": "日付 /Date", "emoji": True},
                "block_id": "date",
            },
            {
                "type": "input",
                "element": {
                    "type": "timepicker",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select time",
                        "emoji": True,
                    },
                    "action_id": "timepicker-action",
                },
                "label": {"type": "plain_text", "text": "時間 /Time", "emoji": True},
                "block_id": "time",
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action",
                },
                "label": {"type": "plain_text", "text": "内容 /Content", "emoji": True},
                "block_id": "text",
            },
        ],
    }
    return view


def view_check_reminder(sceduled_messgae_list, user_id) -> dict[str, Any]:
    blocks = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"<@{user_id}>さんが作成したリマインダーの一覧です。"},
        },
    ]

    for sm in sceduled_messgae_list:
        blocks.append({"type": "divider"})
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": sm}})

    view = {
        "type": "modal",
        "title": {"type": "plain_text", "text": "リマインダーの確認"},
        "blocks": blocks,
    }

    return view


def view_delete_reminder(
    scheduled_message_list: List[Any], user_id: str
) -> dict[str, Any]:
    view = {
        "type": "modal",
        "title": {"type": "plain_text", "text": "リマインダーの削除"},
        "callback_id": "view_reminder_delete",
        "submit": {"type": "plain_text", "text": "削除"},
        "blocks": [
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"<@{user_id}>さんのリマインダーのみが表示されます。\n削除する場合は、1つ選択して *削除* ボタンを押してください。"
                    ),
                },
            },
            {
                "type": "input",
                "block_id": "selected_reminder",
                "element": {
                    "type": "static_select",
                    "options": scheduled_message_list,
                    "action_id": "static_select-action",
                },
                "label": {
                    "type": "plain_text",
                    "text": " ",
                },
            },
        ],
    }

    return view


def view_check(calendar_info: List[Any]) -> dict[str, Any]:
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    "The list of schedules at the tea room is shown below. :memo:\n"
                    "This list is based on the data collected by this bot, "
                    "and may be different from the actual state:exclamation:"
                ),
            },
        },
    ]

    for ci in calendar_info:
        blocks.append({"type": "divider"})
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": ci}})

    view = {
        "type": "modal",
        "callback_id": "view_member",
        "title": {"type": "plain_text", "text": "みんなの予約状況"},
        "blocks": blocks,
    }

    return view


def view_cancel(user_id: str, user_schedule_list: List[Any]) -> dict[str, Any]:
    if len(user_schedule_list) == 0:
        return {
            "type": "modal",
            "title": {"type": "plain_text", "text": "あなたの予約"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<@{user_id}>さんには、削除可能な予約がありませんでした :cry:",
                    },
                },
            ],
        }

    view = {
        "type": "modal",
        "callback_id": "view_cancel_delete",
        "title": {"type": "plain_text", "text": "あなたの予約"},
        "submit": {"type": "plain_text", "text": "削除"},
        "blocks": [
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"<@{user_id}>さんの予約のみが表示されます。\n削除する場合は、予約を1つ選択して *削除* ボタンを押してください。"
                    ),
                },
            },
            {
                "type": "input",
                "block_id": "selected_schedule",
                "element": {
                    "type": "static_select",
                    "options": user_schedule_list,
                    "action_id": "static_select-action",
                },
                "label": {
                    "type": "plain_text",
                    "text": " ",
                },
            },
        ],
    }
    return view


def view_add(
    user_id: str, date: str, start_time: str, end_time: str, description: str
) -> dict[str, Any]:
    reminder_dict = {
        "なし": None,
        "開始時": 0,
        "5分前": 5,
        "10分前": 10,
        "15分前": 15,
        "30分前": 30,
        "1時間前": 60,
        "2時間前": 120,
    }
    reminder_list = [
        {"text": {"type": "plain_text", "text": k}, "value": str(v)}
        for k, v in reminder_dict.items()
    ]
    view = {
        "type": "modal",
        "callback_id": "add_callback",
        "title": {"type": "plain_text", "text": "予約の追加"},
        "submit": {"type": "plain_text", "text": "確定"},
        "close": {"type": "plain_text", "text": "キャンセル"},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"以下の時間帯で予約を追加します\n*{date} {start_time}~{end_time}*",
                },
            },
            {"type": "divider"},
            {
                "type": "input",
                "block_id": "selected_reminder",
                "element": {
                    "type": "static_select",
                    "options": reminder_list,
                    "initial_option": reminder_list[0],
                    "action_id": "static_select-action",
                },
                "label": {
                    "type": "plain_text",
                    "text": "リマインダーを設定：",
                },
            },
        ],
        "private_metadata": json.dumps(
            {
                "user_id": user_id,
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
                "description": description,
            }
        ),
    }
    return view


def view_duplicate(user: str) -> dict[str, Any]:
    view = {
        "type": "modal",
        "close": {"type": "plain_text", "text": "Close", "emoji": True},
        "title": {"type": "plain_text", "text": "予定が重複しています。", "emoji": True},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f":wave: Hey <@{user}>!\n\nSorry, your selected time is already reserved.\n"
                        "Please select another time."
                    ),
                },
            }
        ],
    }
    return view


def view_modal(title: str, text: str, callback_id: Optional[str]) -> dict[str, Any]:
    "Create a modal view by specifying title, text and callback_id"
    view = {
        "type": "modal",
        "close": {"type": "plain_text", "text": "閉じる", "emoji": True},
        "title": {"type": "plain_text", "text": title, "emoji": True},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text,
                },
            }
        ],
    }
    if callback_id:
        view["callback_id"] = callback_id
    return view
