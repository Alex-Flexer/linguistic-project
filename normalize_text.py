from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import pymorphy3

import re
import json


morph = pymorphy3.MorphAnalyzer()
stopwords_ru = stopwords.words("russian")


def normalize_text(text: str) -> list[list[str]]:
    sents = [
        word_tokenize(re.sub(r"\s+", ' ', re.sub(fr"[^а-яa-z0-9]", ' ', sent)))
        for sent in sent_tokenize(text.lower().strip())
    ]
    sents = [
        list(filter(lambda w: w not in stopwords_ru, sent))
        for sent in sents
    ]

    sents = [
        [morph.parse(token)[0].normal_form for token in sent]
        for sent in sents
    ]
    return sents


with open(r"data\prepared\texts.json", 'r', encoding='utf-8') as file:
    channels: dict[str, dict[str, str]] = json.load(file)

for channel_idx, (class_name, content) in enumerate(channels.items()):
    messages = content["messages"]

    for msg_idx, msg in enumerate(messages):
        messages[msg_idx]["text"] = normalize_text(msg["text"])

with open(r"data\prepared\normalized_texts.json", 'w', encoding='utf-8') as file:
    json.dump(channels, file, ensure_ascii=False, indent=2)
