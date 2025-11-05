import json
from collections import Counter


ROUND_BOUND = 6

with open("./data/prepared/texts.json", 'r', encoding='utf-8') as file:
    json_content = json.load(file)


emojis_stat = Counter()

for class_name, content in json_content.items():
    for msg in content["messages"]:
        emojis = msg.get("emojis")
        if emojis:
            for emoji, cnt in emojis.items():
                emojis_stat[emoji.strip()] += cnt

emojis_stat.pop("🫡")

with open("./data/utils/reactions/reactions_categories.json", 'r', encoding='utf-8') as file:
    emojis_cats = json.load(file)["emoji_categories"]

with open("./data/utils/reactions/reactions_titles.json", 'r', encoding='utf-8') as file:
    emojis_titles = json.load(file)

full_emojis_cnt = sum(emojis_stat.values())
cats_emojis_cnt = {
    category["category"]: sum(emojis_stat[emoji] for emoji in category["emojis"])
    for category in emojis_cats
}

emojis_stat = {
    emoji: {
        "title": emojis_titles[emoji],
        "category": category["category"],
        "count": emojis_stat[emoji],
        "global_prop": round(emojis_stat[emoji] / full_emojis_cnt, ROUND_BOUND),
        "category_prop": round(emojis_stat[emoji] / cats_emojis_cnt[category["category"]], ROUND_BOUND)
    }
    for category in emojis_cats for emoji in category["emojis"]
}

with open("./data/utils/reactions/reactions_stat.json", 'w', encoding='utf-8') as file:
    json.dump(emojis_stat, file, indent=2, ensure_ascii=False)
