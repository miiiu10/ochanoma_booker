import datetime
import logging


def send_schedule_message(
    date_time: datetime.datetime, text: str, client, channel
) -> bool:
    "Schedules a message to be sent to a channel"
    try:
        # Call the chat.scheduleMessage method using the WebClient
        result = client.chat_scheduleMessage(
            channel=channel, text=text, post_at=int(date_time.timestamp())
        )
        logging.info(result)  # Log the result
        return True
    except Exception as e:
        logging.error(f"Error scheduling message: {e}")
        return False
