# -*- coding: UTF-8 -*-

import os
import re
import urllib.request
import json


def parse_telegram_links(issue_body:str):
    return list(
        map(
            # trim symbols '<>' from links
            lambda link: re.sub('<|>', '', link),
            # find all links in <...>
            re.findall(r'<https://t.me/[a-zA-Z0-9/_]+>', issue_body)
        )
    )


def get_telegram_message_id(links:list):
    return list(
        map(
            lambda link: link[link.rfind('/')+1:],
            links
        )
    )


def telegram_send_message(
    chat_id:str,
    token:str,
    text:str,
    reply_to_message_ids:list,
    allow_sending_without_reply:bool,
    parse_mode:str
    ):
    for id in reply_to_message_ids:
        try:
            request = urllib.request.Request(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json.dumps(
                    {
                        "chat_id": chat_id,
                        "text": text,
                        "reply_to_message_id": id,
                        "allow_sending_without_reply": allow_sending_without_reply,
                        "parse_mode": parse_mode,
                    }
                ).encode("utf-8"),
                {
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(request) as f:
                response = f.read()
            return response
        except Exception as e:
            print(e)


links = parse_telegram_links(os.getenv('GITHUB_ISSUE_BODY'))
print("-> Parsed links:")
print(*links, sep='\n')
print()

messages_id = get_telegram_message_id(links)
print("-> Messages ID's to reply:")
print(*messages_id, sep='\n')
print()

response = telegram_send_message(
    os.getenv('TELEGRAM_CHAT_ID'),
    os.getenv('TELEGRAM_BOT_TOKEN'),
    os.getenv('TELEGRAM_MESSAGE_TEMPLATE'),
    messages_id,
    os.getenv('TELEGRAM_ALLOW_SENDING_WITHOUT_REPLY'),
    os.getenv('TELEGRAM_PARSE_MODE'),
)
print(response.decode())
