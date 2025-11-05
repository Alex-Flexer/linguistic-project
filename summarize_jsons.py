import os
import json

PATH = './data/original jsons'

files = os.listdir(PATH)
full_json = {}

for filename in files:
    if not filename.endswith(".json") or not filename[0].isdigit():
        continue

    filepath = os.path.join(PATH, filename)

    with open(filepath, 'r', encoding='utf-8') as file:
        json_content: dict = json.load(file)

    messages = []

    for msg in json_content["messages"]:
        if msg["type"] != "message" or msg["text"] == '':
            continue

        messages.append({
            "text": ''.join(text if isinstance(text, str) else text["text"]
                            for text in msg["text"]),
            "emojis": {
                react["emoji"]: react["count"]
                for react in msg.get("reactions", [])
                if react["type"] == "emoji"
            }
        })

    class_name = filename.removesuffix(".json")
    full_json[class_name] = {"messages": messages}


with open("./data/prepared/texts.json", 'w', encoding='utf-8') as file:
    json.dump(full_json, file, ensure_ascii=False, indent=2)
