import datetime
from typing import Optional, Tuple


def send_schedule_message(
    date_time: datetime.datetime, text: str, client, channel
) -> Tuple[Optional[dict], Optional[bool]]:
    "Schedules a message to be sent to a channel"
    try:
        # Call the chat.scheduleMessage method using the WebClient
        # https://api.slack.com/methods/chat.scheduleMessage
        result = client.chat_scheduleMessage(
            channel=channel,
            text=text,
            post_at=int(date_time.timestamp()),
        )
        if result["ok"]:
            return (result, None)
        else:
            return (None, f"リマインダーの設定には以下の理由で失敗してしまいました：\n{result['error']}")

    except Exception as e:
        return (None, f"リマインダーの設定には以下の理由で失敗してしまいました：\n{e}")


def list_scheduled_messages(client) -> Tuple[Optional[list], Optional[bool]]:
    "List scheduled messages using latest and oldest timestamps"
    # https://api.slack.com/methods/chat.scheduledMessages.list
    try:
        # Call the chat.scheduledMessages.list method using the WebClient
        result = client.chat_scheduledMessages_list(
            oldest=str(int(datetime.datetime.now().timestamp()))
        )

        # Print scheduled messages
        for message in result["scheduled_messages"]:
            print(message)

        if result["ok"]:
            return (result["scheduled_messages"], None)
        else:
            return (None, f"リマインダーの確認には以下の理由で失敗してしまいました：\n{result['error']}")

    except Exception as e:
        return (None, f"リマインダーの確認には以下の理由で失敗してしまいました：\n{e}")
