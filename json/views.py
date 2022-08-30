def view_home(user):
    view = {
            "type": "home",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "お茶の間予約システム"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (f"<@{user}>さん、ここでお茶の間の予約をしてみよう！ :calendar:\n"
                                 "予約状況は <https://calendar.google.com/calendar/u/0?cid=Y19uNzNwbGVzZWtxYXRzanU2aDFjcTFibjJhc0Bncm91cC5jYWxlbmRhci5nb29nbGUuY29t|*ここ*>から見れます！\n")
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "input",
                    "element": {
                        "type": "datepicker",
                        #"initial_date": "2022-08-01",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a date"
                        },
                        "action_id": "datepick"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "日付",
                        "emoji": True
                    },
                    "block_id": "dateblock"
                },
                {
                    "type": "input",
                    "element": {
                            "type": "timepicker",
                            #"initial_time": "00:00",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select start time"
                            },
                            "action_id": "timepick"
                        },
                    "label": {
                        "type": "plain_text",
                        "text": "時間",
                        "emoji": True
                    },
                    "block_id": 'timeblock'
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "[注]分刻みの場合は直接入力する事ができるよ！"
                    }
                },
                {
                    "type": "input",
                    "element": {
                            "type": "plain_text_input",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Write description"
                            },
                            "action_id": "description"
                        },
                    "label": {
                        "type": "plain_text",
                        "text": "詳細",
                        "emoji": True
                    },
                    "block_id": 'textblock'
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "style": "primary",
                            "text": {
                                "type": "plain_text",
                                "text": "追加"
                            },
                            "value": "home_add",
                            "action_id": "add_home"
                        }
                    ]
                },
                {
                    "type": "input",
                    "element": {
                            "type": "plain_text_input",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Write eventID"
                            },
                            "action_id": "delete_id"
                        },
                    "label": {
                        "type": "plain_text",
                        "text": "消去したい予約のIDを入力してください。",
                        "emoji": True
                    },
                    "block_id": 'deleteblock'
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "style": "primary",
                            "text": {
                                "type": "plain_text",
                                "text": "削除"
                            },
                            "value": "home_delete",
                            "action_id": "delete_home",
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "確認"
                            },
                            "value": "home_check",
                            "action_id": "check_home"
                        }
                    ]
                }
            ]
        }

    return view

def view_schedule(text):
    view={
            "type": "modal",
            "callback_id": "view_before",
            "title": {"type": "plain_text", "text":"Schedule"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ("checking schedule")}
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text
                    }
                }
            ]
        }

    return view

def view_record(text1, text2, url):
    view={
            "type": "modal",
            "callback_id": "view_record",
            "title": {"type": "plain_text", "text":"Time Report"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text1}
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text2
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Record"
                        },
                        "value": "url",
                        "action_id": "button-url",
                        "style": "primary",
                        "url": url
                    }
                }
            ]
        }

    return view

def view_check(calendar_info):
    view={
            "type": "modal",
            "callback_id": "view_member",
            "title": {"type": "plain_text", "text":"Schedules :eyes:"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ("The list of schedules at the tea room is shown below. :memo:\n"
                                 "This list is based on the data collected by this bot, and may be different from the actual state:exclamation:")}
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": calendar_info
                        }
                }
            ]
        }

    return view
