"""
file:         telegram-chat-parser.py
author:       Artur Rodrigues Rocha Neto
email:        artur.rodrigues26@gmail.com
github:       https://github.com/keizerzilla
created:      23/12/2020
description:  Script to parse a Telegram chat history JSON file into a tabular format (CSV).
requirements: Python 3.x
"""

import re
import sys
import csv
import json
from datetime import datetime

COLUMNS = [
    "date",
    "msg_content",
]

FILE_TYPES = [
    "animation",
    "video_file",
    "video_message",
    "voice_message",
    "audio_file",
]

MENTION_TYPES = [
    "mention",
    "mention_name",
]

NULL_NAME_COUNTER = 0

tatar_alphabet = 'А а Ә ә Б б В в Г г Д д Е е Ё ё Ж ж Җ җ З з И и Й й К к Л л М м Н н Ң ң О о Ө ө П п Р р С с Т т У у Ү ү Ф ф Х х Һ һ Ц ц Ч ч Ш ш Щ щ Ъ ъ Ы ы Ь ь Э э Ю ю Я я'.split()

russian_alphabet = 'А а Б б В в Г г Д д Е е Ё ё Ж ж З з И и Й й К к Л л М м Н н О о П п Р р С с Т т У у Ф ф Х х Ц ц Ч ч Ш ш Щ щ Ъ ъ Ы ы Ь ь Э э Ю ю Я я'.split()

def filter_text(text):
    filtered_text = []
    for letter in text:
        if letter == ' ' or letter in tatar_alphabet or letter in russian_alphabet:
            filtered_text.append(letter)
    return re.sub(' +', ' ', ''.join(filtered_text))

def get_chat_name(jdata):
    global NULL_NAME_COUNTER
    if jdata.get("name") is None:
        NULL_NAME_COUNTER += 1
        return f"UnnamedChat-{NULL_NAME_COUNTER}"
    return re.sub(r'[\W_]+', u'', jdata.get("name"), flags=re.UNICODE)


def process_message(message):
    if message["type"] != "message":
        return None

    msg_id = message["id"]
    sender = message["from"]
    sender_id = message["from_id"]
    reply_to_msg_id = message.get("reply_to_message_id", -1)
    date = message["date"].replace("T", " ")
    dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    msg_content = message.get("text", "")
    msg_type = "text"

    if "media_type" in message:
        msg_type = message["media_type"]
        if message["media_type"] == "sticker":
            if "sticker_emoji" in message:
                msg_content = message["file"]
            else:
                msg_content = "?"
        elif message["media_type"] in FILE_TYPES:
            msg_content = message["file"]
    elif "file" in message:
        msg_type = "file"
        msg_content = message["file"]

    if "photo" in message:
        msg_type = "photo"
        # msg_content = message["text"]
    elif "poll" in message:
        msg_type = "poll"
        msg_content = str(message["poll"]["total_voters"])
    elif "location_information" in message:
        msg_type = "location"
        loc = message["location_information"]
        msg_content = f"{loc['latitude']},{loc['longitude']}"

    has_mention = 0
    has_email = 0
    has_phone = 0
    has_hashtag = 0
    is_bot_command = 0

    if isinstance(msg_content, list):
        txt_content = ""
        for part in msg_content:
            if isinstance(part, str):
                txt_content += part
            elif isinstance(part, dict):
                if part["type"] == "link":
                    msg_type = "link"
                elif part["type"] in MENTION_TYPES:
                    has_mention = 1
                elif part["type"] == "email":
                    has_email = 1
                elif part["type"] == "phone":
                    has_phone = 1
                elif part["type"] == "hashtag":
                    has_hashtag = 1
                elif part["type"] == "bot_command":
                    is_bot_command = 1

                txt_content += part["text"]
        msg_content = txt_content

    msg_content = msg_content.replace("\n", " ")

    if msg_content == '' or msg_content == '(File not included. Change data exporting settings to download.)' or msg_type == 'poll':
        return None

    return {
        "date": date,
        "msg_content": filter_text(msg_content),
    }


def parse_telegram_to_csv(jdata):
    chat_name = get_chat_name(jdata)
    output_filepath = 'output.csv'

    with open(output_filepath, "w", encoding="utf-8-sig", newline="") as output_file:
        writer = csv.DictWriter(output_file, COLUMNS, dialect="unix", quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()

        for message in jdata["messages"]:
            row = process_message(message)
            if row is not None:
                writer.writerow(row)

    print(chat_name, "OK!")


if __name__ == "__main__":
    output = 'table.csv'
    backup_filepath = 'result.json'

    with open(backup_filepath, "r", encoding="utf-8-sig") as input_file:
        contents = input_file.read()
        jdata = json.loads(contents)

        if "chats" not in jdata:
            parse_telegram_to_csv(jdata)
        else:
            for chat in jdata["chats"]["list"]:
                parse_telegram_to_csv(chat)
