import os
import os.path as osp
import re
import sys
import errno
from configparser import ConfigParser
import logging

from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

logging.basicConfig(level=logging.DEBUG)

sys.path.append(osp.join(osp.dirname(osp.abspath(__file__)), 'json'))
#from blocks import block_other
from views import view_home, view_check
from modules import manage_info, schedule2txt
from calendarFunc import insert, get, delete

config = ConfigParser()
config_path = './bolt_config.ini'
if not os.path.exists(config_path):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_path)
config.read(config_path)

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

# ショートカットとモーダル
@app.shortcut("socket-mode-shortcut")
def handle_shortcut(ack, body: dict, client: WebClient):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "modal-id",
            "title": {"type": "plain_text", "text": "タスク登録"},
            "submit": {"type": "plain_text", "text": "送信"},
            "close": {"type": "plain_text", "text": "キャンセル"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "input-task",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "input",
                        "multiline": True,
                        "placeholder": {
                            "type": "plain_text",
                            "text": "タスクの詳細・期限などを書いてください",
                        },
                    },
                    "label": {"type": "plain_text", "text": "タスク"},
                }
            ],
        },
    )

@app.view("modal-id")
def handle_view_submission(ack, view, logger):
    logger.info(f"Submitted data: {view['state']['values']}")
    ack()

@app.action("add_home")
def handle_some_action(ack, body, client):
    ack()
    user = body['user']['id']
    date = body['view']['state']['values']['dateblock']['datepick']['selected_date']
    time = body['view']['state']['values']['timeblock']['timepick']['selected_time']
    description = body['view']['state']['values']['textblock']['description']['value']
    client.views_open(
        trigger_id=body["trigger_id"],
        view=manage_info(user, add=True, date=date, time=time, description=description)
    )

@app.action("delete_home")
def action_member(ack, body, client):
    ack()
    user = body['user']['id']
    id = body['view']['state']['values']['deleteblock']['delete_id']['value']
    client.views_open(
        trigger_id=body["trigger_id"],
        view=manage_info(user, add=False, event_id=id)
    )

@app.action("check_home")
def action_member(ack, body, client):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view=view_check(schedule2txt(get()))
    )

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, config['DEFAULT']['slack_app_token']).start()