import os
import os.path as osp
import re
import sys
import errno
from configparser import ConfigParser
import logging

from slack_sdk import WebClient
from slack_bolt import App, Ack
from slack_bolt.adapter.socket_mode import SocketModeHandler

#CHANNEL_ID = "#apptest"
CHANNEL_ID = "#お茶室予約"

logging.basicConfig(level=logging.DEBUG)

sys.path.append(osp.join(osp.dirname(osp.abspath(__file__)), 'json'))
#from blocks import block_other
from views import view_delete_fail, view_duplicate, view_home, view_check, view_schedule, view_cancel
from modules import manage_info, schedule2txt, delete_from_chat, schedule2list
from calendarFunc import insert, get, delete

config = ConfigParser()
config_path = './bolt_config.ini'
if not os.path.exists(config_path):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_path)
config.read(config_path)

def get_end_time(time):
    s_hour, s_minute = map(int, time.split(':'))
    e_hour = s_hour + 1
    return f'{e_hour:0=2}:{s_minute:0=2}'

# Initializes your app with your bot token and socket mode handler
app = App(token=config['DEFAULT']['token'])

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

# Listens to incoming messages that contain "hello"
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
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
    # Acknowledge the action
    ack()
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

    check_frag = manage_info(user, add=True, date=date, start_time=start_time, end_time=end_time, description=description)
    if check_frag:
        schedules = get()
        ui = view_schedule(schedule2txt(schedules))
        client.chat_postMessage(
            channel=CHANNEL_ID,
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
        date, time = text.split()
        date = date[-10:]   # 2022-02-23
        time = time[:11]    # 12:00~14:30

        check_frag = delete_from_chat(click_user, date, time)
        if check_frag:
            say(f"<@{body['user']['id']}> が予約を消しました。")

    else:
        say("他の人の予約は消せません。")

@app.action("delete_home")
def action_member(ack, body, client):
    ack()
    user = body['user']['id']
    id = body['view']['state']['values']['deleteblock']['delete_id']['value']
    check_frag = manage_info(user, add=False, event_id=id)
    if check_frag:
        schedules = get()
        ui = view_schedule(schedule2txt(schedules))
    else:
        ui = view_delete_fail(user)
    client.views_open(
        trigger_id=body["trigger_id"],
        view=ui
    )

@app.action("check_home")
def action_member(ack, body, client):
    ack()
    user_id = body['user']['id']
    user_schedule_list = schedule2list(user_id, get())
    client.views_open(
        trigger_id=body["trigger_id"],
        # view=view_check(schedule2txt(get()))
        view=view_cancel(user_id, user_schedule_list)
    )

# view.callback_id にマッチングする（正規表現も可能）
@app.view("view_cancel_delete")
def handle_view_cancel_events(ack: Ack, view: dict, client: WebClient):
    # TODO: 正しく取得できるか確認
    event_id = view["state"]["values"]["selected_schedule"]["action_id"]["static_select-action"]
    # まず「処理中...」である旨を伝えます
    ack(
        response_action="update",
        view={
            "type": "modal",
            "callback_id": "modal-id",
            "title": {"type": "plain_text", "text":"Schedules :eyes:"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "処理中です... このモーダルを閉じずにしばらくお待ちください :bow:",
                    },
                }
            ],
        },
    )

    delete(event_id)

    # 結果を待った後 views.update API を非同期で呼び出して再度更新をかけます
    client.views_update(
        view_id=view.get("id"),
        view={
            "type": "modal",
            # "callback_id": "modal-id",
            "title": {"type": "plain_text", "text":"Schedules :eyes:"},
            "close": {"type": "plain_text", "text": "閉じる"},
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "plain_text", "text": "正常に完了しました！"},
                }
            ],
        },
    )

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, config['DEFAULT']['slack_app_token']).start()