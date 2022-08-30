def block_before(text, url):
    block = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*You entered 'BEFORE' last time. Is it correct?*",
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
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

    return block

def block_after(text, url):
    block = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*You entered 'AFTER' last time. Is it correct?*",
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
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

    return block

def block_record(text, url):
    block = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
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

    return block

def block_other(text):
    block = [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": text,
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "style": "primary",
                            "text": {
                                "type": "plain_text",
                                "text": "Before"
                            },
                            "value": "before",
                            "action_id": "before"
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "text": {
                                "type": "plain_text",
                                "text": "After"
                            },
                            "value": "after",
                            "action_id": "after"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Member"
                            },
                            "value": "member",
                            "action_id": "member"
                        }
                    ]
                }
            ]

    return block