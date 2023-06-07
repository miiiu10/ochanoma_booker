import os
import re
from dotenv import load_dotenv
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from views import view_duplicate, view_home, view_check, view_schedule, view_cancel
from modules import manage_info, schedule2txt, delete_from_chat, schedule2list
from calendarFunc import get, delete

logging.basicConfig(level=logging.DEBUG)

# Load .env file as environment varialble
load_dotenv(f".env.{os.getenv('env')}")

# Initializes your app with your bot token and socket mode handler
app = App(token=os.getenv('TOKEN'))


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        # 組み込みのクライアントを使って views.publish を呼び出す
        client.views_publish(
            # イベントに関連づけられたユーザー ID を使用
            user_id=event["user"],
            # アプリの設定で予めホームタブが有効になっている必要がある
            view=view_home(event["user"])
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.message("hello")
def message_hello(message, say):
    "Listen to incoming messages that contain 'hello'"
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )


@app.action("button_click")
def action_button_click(body, ack, say):
    ack()   # Acknowledge the action
    say(f"<@{body['user']['id']}> clicked the button")


@app.action("add_home")
def handle_some_action(ack, body, client):
    ack()
    user = body['user']['id']
    date = body['view']['state']['values']['dateblock']['datepick']['selected_date']
    start_time = body['view']['state']['values']['start_time_block']['timepick']['selected_time']
    end_time = body['view']['state']['values']['end_time_block']['timepick']['selected_time']
    # 入力がされなかった時の表示用
    if end_time==None:
        start_hour, start_minute = map(int, start_time.split(":"))
        end_time = "{:02}:{:02}".format(start_hour+1, start_minute)
    description = body['view']['state']['values']['textblock']['description']['value']

    check_flag = manage_info(user, add=True, date=date, start_time=start_time, end_time=end_time, description=description)
    if check_flag:
        schedules = get()
        ui = view_schedule(schedule2txt(schedules))
        client.chat_postMessage(
            channel=os.getenv("CHANNEL_ID"),
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"<@{body['user']['username']}>が{date} {start_time}~{end_time}に621の会議室を予約しました。"}, # ここを変える時はaction_button_clickも変更
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "delete"},
                        "action_id": "delete_botton"
                    }
                }
            ]
        )
    else:
        ui = view_duplicate(user)
    client.views_open(
        trigger_id=body["trigger_id"],
        view=ui
    )

@app.action("delete_botton")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    click_user = body['user']['id']
    chat_user = re.search('<@(.*?)>', body['message']['text']).group(1)

    if click_user==chat_user:
        # メッセージから時間を取得
        # チャットへのメッセージを変更したらここも変更
        text = body['message']['text']
        splited_text = list(text.split())
        # TODO: 正規表現を用いる
        date_str = splited_text[0][-10:]  # 2022-02-23
        time_str = splited_text[1][:11]    # 12:00~14:30

        check_flag = delete_from_chat(click_user, date_str, time_str)
        if check_flag:
            say(f"<@{body['user']['id']}> が予約を取り消しました。")

    else:
        say("他の人の予約は消せません。")

@app.action("delete_home")
def action_member(ack, body, client):
    ack()
    user_id = body['user']['id']
    client.views_open(
        trigger_id=body["trigger_id"],
        view=view_cancel(user_id, schedule2list(user_id, get()))
    )

@app.action("check_home")
def action_member(ack, body, client):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view=view_check(schedule2txt(get()))
    )

@app.view("view_cancel_delete")
def handle_view_events(ack, body, logger):
    event_id = body["view"]["state"]["values"]["selected_schedule"]["static_select-action"]["selected_option"]["value"]

    err = delete(event_id)
    msg = "予約が正常に取り消されました" if err != False else "エラーが発生しました。\n再度お試しいただくか、管理者までお問い合わせください。"

    ack(
        response_action="update",
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text":"予約の削除 :wastebasket:"},
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


# Start app
if __name__ == "__main__":

    SocketModeHandler(app, os.getenv('SLACK_APP_TOKEN')).start()