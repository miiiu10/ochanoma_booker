import datetime
from typing import Optional, Tuple
from slack_sdk.web.client import WebClient
from slack_sdk.errors import SlackApiError


def send_schedule_message(
    date_time: datetime.datetime, text: str, client: WebClient, channel: str
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
        return (result, None)
    except SlackApiError as e:  # Explainable errors
        if e.response["error"] == "time_in_past":
            return (None, "未来の日時を入力してください。")
        else:
            return (None, f"リマインダーの設定には以下の理由で失敗してしまいました：\n{e.response['error']}")
    except Exception as e:
        return (None, f"リマインダーの設定には以下の理由で失敗してしまいました：\n{e}")


def list_scheduled_messages(client: WebClient) -> Tuple[Optional[list], Optional[bool]]:
    "List scheduled messages using latest and oldest timestamps"
    try:
        # Call the chat.scheduledMessages.list method using the WebClient
        # https://api.slack.com/methods/chat.scheduledMessages.list
        result = client.chat_scheduledMessages_list(
            oldest=str(int(datetime.datetime.now().timestamp()))
        )
        # Print scheduled messages
        # for message in result["scheduled_messages"]:
        #     print(message)
        return (result["scheduled_messages"], None)

    except SlackApiError as e:  # Explainable errors
        return (None, f"リマインダーの確認には以下の理由で失敗してしまいました：\n{e.response['error']}")
    except Exception as e:
        return (None, f"リマインダーの確認には以下の理由で失敗してしまいました：\n{e}")


def delete_scheduled_message(client: WebClient, scheduled_message_id: str, channel_id: str) -> Tuple[Optional[dict], Optional[bool]]:
    "Delete a pending scheduled message from the queue."
    try:
        # Call the chat.deleteScheduledMessage method using the built-in WebClient
        # https://api.slack.com/methods/chat.deleteScheduledMessage
        result = client.chat_deleteScheduledMessage(
            channel=channel_id,
            scheduled_message_id=scheduled_message_id
        )
        return (result, None)
    except SlackApiError as e:  # Explainable errors
        if e.response["error"] == "channel_not_found":
            return (None, "リマインドするチャンネルが無効または存在しません。")
        if e.response["error"] == "invalid_scheduled_message_id":
            return (None, "リマインダーがすでに送信または削除されました。")
        else:
            return (None, f"リマインダーの削除には以下の理由で失敗してしまいました：\n{e.response['error']}")
    except Exception as e:
        return (None, f"リマインダーの削除には以下の理由で失敗してしまいました：\n{e}")
