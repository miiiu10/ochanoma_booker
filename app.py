import datetime
import json
import os
import re
from typing import Any, Dict, Optional
from dotenv import load_dotenv
import logging

from slack_bolt import App
from slack_bolt.context.ack import Ack
from slack_bolt.context.say import Say
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web.client import WebClient
from scheduling import (
    delete_scheduled_message,
    list_scheduled_messages,
    send_schedule_message,
)

from views import (
    view_add,
    view_add_reminder,
    view_check_reminder,
    view_delete_reminder,
    view_home,
    view_check,
    view_modal,
    view_cancel,
)
from modules import (
    add_reservation,
    schedule2txt,
    delete_from_chat,
    schedule2list,
    validate_input,
)
from calendarFunc import get, delete


# Logging settings
loging_level = logging.DEBUG
if os.getenv("env") == "prod":
    loging_level = logging.WARNING
logging.basicConfig(level=loging_level)

# Load .env file as environment varialble
load_dotenv(".env")  # Google Calenar scopes and ID
env_file_path = ".env.dev"
if os.getenv("env"):
    env_file_path = f".env.{os.getenv('env')}"
load_dotenv(env_file_path)  # Slack App tokens


# Initializes your app with your bot token and socket mode handler
app = App(token=os.getenv("TOKEN"))


@app.event("app_home_opened")
def event_home_tab(client: WebClient, event: Optional[Dict[str, Any]], logger: logging.Logger):
    try:
        # 組み込みのクライアントを使って views.publish を呼び出す
        client.views_publish(
            user_id=event["user"],  # イベントに関連づけられたユーザー ID を使用
            view=view_home(user_id=event["user"]),  # アプリの設定で予めホームタブが有効になっている必要がある
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.event("message")
def event_dm_menu(say: Say, message: Optional[Dict[str, Any]], ack: Ack):
    "Show the menu when menshioned in DM"
    if message["channel_type"] == "im":
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<@{message['user']}>さん、こんにちは！\n:alarm_clock:リマインダー機能に関して何かお困りですか？",
                    },
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":calendar:「新しいリマインダーを追加したい」なら...",
                    },
                    "accessory": {
                        "type": "button",
                        "style": "primary",
                        "text": {"type": "plain_text", "text": "追加"},
                        "action_id": "reminder_add",
                    },
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": ":eyes:「リマインダーの一覧を確認したい」なら..."},
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "確認"},
                        "action_id": "reminder_check",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":wastebasket:「作成したリマインダーを削除したい」なら...",
                    },
                    "accessory": {
                        "type": "button",
                        "style": "danger",
                        "text": {"type": "plain_text", "text": "削除"},
                        "action_id": "reminder_delete",
                    },
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "他に分からないことがあれば、何でも管理者に聞いてください！"},
                },
            ],
            text=f"<@{message['user']}>さん、こんにちは！\n何かお困りですか？",
        )
    else:
        ack()


@app.action("reminder_add")
def action_dm_add_reminder(ack: Ack, body: Dict[str, Any], client: WebClient):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view=view_add_reminder(user_id=body["user"]["id"]),
    )


@app.action("reminder_check")
def action_dm_check_reminder(ack: Ack, body: Dict[str, Any], client: WebClient):
    ack()
    result, err = list_scheduled_messages(client=client)
    if err:
        result_view = view_modal(title="リマインダーの確認", text=str(err), callback_id=None)
    else:
        if len(result) == 0:
            result_view = view_modal(
                title="リマインダーの確認",
                text=f"<@{body['user']['id']}>さんが作成したリマインダーはありません。",
                callback_id=None,
            )
        else:
            scheduled_message_list = []
            for scheduled_message in result:
                if scheduled_message["channel_id"] == body["channel"]["id"]:
                    post_time_dt = datetime.datetime.fromtimestamp(
                        scheduled_message["post_at"]
                    )
                    created_time_dt = datetime.datetime.fromtimestamp(
                        scheduled_message["date_created"]
                    )
                    scheduled_message_list.append(
                        (
                            f"リマインド日時: {post_time_dt.date()} {str(post_time_dt.time())[:5]}\n"
                            f"作成日時: {created_time_dt.date()} {str(created_time_dt.time())[:5]}\n"
                            f"メッセージ: {scheduled_message['text']}"
                        )
                    )
            result_view = view_check_reminder(
                sceduled_messgae_list=scheduled_message_list, user_id=body["user"]["id"]
            )
    client.views_open(trigger_id=body["trigger_id"], view=result_view)


@app.action("reminder_delete")
def action_dm_delete_reminder(ack: Ack, body: Dict[str, Any], client: WebClient):
    ack()
    result, err = list_scheduled_messages(client=client)
    if err:
        result_view = view_modal(title="リマインダーの削除", text=str(err), callback_id=None)
    else:
        if len(result) == 0:
            result_view = view_modal(
                title="リマインダーの削除",
                text=f"<@{body['user']['id']}>さんが作成したリマインダーはありません。",
                callback_id=None,
            )
        else:
            scheduled_message_list = []
            for scheduled_message in result:
                if scheduled_message["channel_id"] == body["channel"]["id"]:
                    post_time_dt = datetime.datetime.fromtimestamp(
                        scheduled_message["post_at"]
                    )
                    option_text = (
                        f"リマインド日時: {post_time_dt.date()} {str(post_time_dt.time())[:5]}\n"
                        f"メッセージ: {scheduled_message['text']}"
                    )
                    if len(option_text) >= 76:  # must be less than 76 characters
                        option_text = option_text[:74] + "…"
                    scheduled_message_list.append(
                        {
                            "text": {
                                "type": "plain_text",
                                "text": option_text,
                            },
                            "value": f"{scheduled_message['id']} {scheduled_message['channel_id']}",
                        }
                    )
            result_view = view_delete_reminder(
                scheduled_message_list=scheduled_message_list,
                user_id=body["user"]["id"],
            )

    # user_id = body["user"]["id"]
    client.views_open(trigger_id=body["trigger_id"], view=result_view)


@app.action("add_home")
def action_home_add_reservation(ack: Ack, body: Dict[str, Any], client: WebClient):
    "Add a reservation by clicking the button in home tab"
    ack()

    # Extract information from body
    user_id = body["user"]["id"]
    date = body["view"]["state"]["values"]["dateblock"]["datepick"]["selected_date"]
    start_time = body["view"]["state"]["values"]["start_time_block"]["timepick"][
        "selected_time"
    ]
    end_time = body["view"]["state"]["values"]["end_time_block"]["timepick"][
        "selected_time"
    ]
    description = body["view"]["state"]["values"]["textblock"]["description"]["value"]

    # Validation
    err, response = validate_input(user_id, date, start_time, end_time, description)
    if err:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=view_modal(title="エラー", text=response, callback_id=None),
        )
    else:
        end_time = response
        client.views_open(
            trigger_id=body["trigger_id"],
            view=view_add(
                user_id=user_id,
                date=date,
                start_time=start_time,
                end_time=end_time,
                description=description,
            ),
        )


@app.action("delete_button")
def action_channel_delete_reservation(body: Dict[str, Any], ack: Ack, say):
    ack()
    click_user = body["user"]["id"]
    chat_user = re.search("<@(.*?)>", body["message"]["text"]).group(1)

    if click_user == chat_user:
        # メッセージから時間を取得
        # チャットへのメッセージを変更したらここも変更
        text = body["message"]["text"]
        splited_text = list(text.split())
        # TODO: 正規表現を用いる
        date_str = splited_text[0][-10:]  # 2022-02-23
        time_str = splited_text[1][:11]  # 12:00~14:30

        check_flag = delete_from_chat(click_user, date_str, time_str)
        if check_flag:
            say(f"<@{body['user']['id']}> が予約を取り消しました。")

    else:
        say("他の人の予約は消せません。")


@app.action("check_home")
def action_home_check_reservation(ack: Ack, body: Dict[str, Any], client: WebClient):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"], view=view_check(schedule2txt(get()))
    )


@app.action("delete_home")
def action_home_delete_reservation(ack: Ack, body: Dict[str, Any], client: WebClient):
    ack()
    user_id = body["user"]["id"]
    client.views_open(
        trigger_id=body["trigger_id"],
        view=view_cancel(user_id, schedule2list(user_id, get())),
    )


@app.view("add_callback")
def view_home_add_reservation(ack: Ack, body: Dict[str, Any], client: WebClient):
    reminder_minutes = body["view"]["state"]["values"]["selected_reminder"][
        "static_select-action"
    ]["selected_option"]["value"]
    metadata_dict = json.loads(body["view"]["private_metadata"])

    # Add a reservation using Google Calendar API
    calendar_result, err = add_reservation(
        user_id=metadata_dict["user_id"],
        date=metadata_dict["date"],
        start_time=metadata_dict["start_time"],
        end_time=metadata_dict["end_time"],
        description=metadata_dict["description"],
    )

    if err:
        result_view = view_modal(
            title="エラー", text=f"\n:warning: {err}", callback_id=None
        )
        ack(response_action="update", view=result_view)
    else:
        start_time = datetime.datetime.fromisoformat(
            calendar_result["start"]["dateTime"]
        )
        end_time = datetime.datetime.fromisoformat(calendar_result["end"]["dateTime"])
        date_time_str = f"{start_time.date()} {str(start_time.time())[:5]}~{str(end_time.time())[:5]}"

        modal_message = f":white_check_mark: {date_time_str} に621の会議室を予約しました。"

        if reminder_minutes:
            reminder_date_time = start_time - datetime.timedelta(
                minutes=int(reminder_minutes)
            )
            reminder_result, err = send_schedule_message(
                date_time=reminder_date_time,
                text=f"<@{body['user']['username']}>さんは {date_time_str} に621の会議室を予約しています。忘れないようにしてください！",
                client=client,
                channel=metadata_dict[
                    "user_id"
                ],  # https://api.slack.com/methods/chat.scheduleMessage#channels__post-to-a-dm
            )
            if err:
                modal_message += f"\n:warning: {err}"
            else:
                reminder_date_time_str = (
                    f"{reminder_date_time.date()} {str(reminder_date_time.time())[:5]}"
                )
                modal_message += f"\n:white_check_mark: {reminder_date_time_str} になったらOchanomaBookerの「メッセージ」タブでリマインドします。"

        result_view = view_modal(title="予約の追加", text=modal_message, callback_id=None)
        ack(response_action="update", view=result_view)

        client.chat_postMessage(
            channel=os.getenv("CHANNEL_ID"),
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            f"<@{body['user']['username']}>が"
                            f"{date_time_str}"
                            "に621の会議室を予約しました"
                        ),
                    },  # ここを変える時はaction_delete_button_clickも変更
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "delete"},
                        "action_id": "delete_button",
                    },
                }
            ],
        )


@app.view("view_reminder_add")
def view_dm_add_reminder(ack: Ack, body: Dict[str, Any], client: WebClient):
    reminder_date = body["view"]["state"]["values"]["date"]["datepicker-action"]["selected_date"]
    reminder_time = body["view"]["state"]["values"]["time"]["timepicker-action"]["selected_time"]
    content = body["view"]["state"]["values"]["text"]["plain_text_input-action"]["value"]
    reminder_date_time_str = f'{reminder_date} {reminder_time}'
    reminder_date_time = datetime.datetime.fromisoformat(reminder_date_time_str)

    reminder_result, err = send_schedule_message(
        date_time=reminder_date_time,
        text=f"<@{body['user']['id']}>さん、{content}の時間です！忘れないようにしてください。",
        client=client,
        channel=body['user']['id']
    )
    if err:
        modal_message = f":warning: {err}"
    else:
        modal_message = f":white_check_mark: {reminder_date_time_str} になったらOchanomaBookerの「メッセージ」タブでリマインドします。"

    result_view = view_modal(title="リマインダーの追加", text=modal_message, callback_id=None)
    ack(response_action="update", view=result_view)


@app.view("view_cancel_delete")
def view_home_delete_reservation(ack: Ack, body: Dict[str, Any]):
    event_id = body["view"]["state"]["values"]["selected_schedule"][
        "static_select-action"
    ]["selected_option"]["value"]

    err = delete(event_id)
    if err:
        msg = "エラーが発生しました。\n再度お試しいただくか、管理者までお問い合わせください。"
    else:
        msg = "予約が正常に取り消されました"

    ack(
        response_action="update",
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": "予約の削除 :wastebasket:"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": msg,
                    },
                }
            ],
        },
    )


@app.view("view_reminder_delete")
def view_dm_delete_reminder(ack: Ack, body: Dict[str, Any], client: WebClient):
    scheduled_message_id, channel_id = body["view"]["state"]["values"][
        "selected_reminder"
    ]["static_select-action"]["selected_option"]["value"].split()

    result, err = delete_scheduled_message(
        client=client, scheduled_message_id=scheduled_message_id, channel_id=channel_id
    )
    if err:
        msg = f"以下のエラーが発生しました。\n{err}\n再度お試しいただくか、管理者までお問い合わせください。"
    else:
        msg = "予約が正常に取り消されました"

    ack(
        response_action="update",
        view=view_modal(title="リマインダーの削除", text=msg, callback_id=None),
    )


# Start app
if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
