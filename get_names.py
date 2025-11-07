import json
from pymorphy3 import MorphAnalyzer
from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    PER,
    Doc
)

morph = MorphAnalyzer()
segmenter = Segmenter()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

def is_name_or_surname_or_patronymic(word):
    parsed = morph.parse(word)
    if not parsed:
        return False

    tag = parsed[0].tag
    normal_form = parsed[0].normal_form

    if 'Name' in tag:
        return True
    if 'Surn' in tag:
        return True
    if 'Patr' in tag:
        return True

    if normal_form.endswith('ич') or normal_form.endswith('на'):
        if len(normal_form) > 3 and normal_form[-3:] in ['вич', 'вна', 'вича', 'вну']:
            return True
        if normal_form in ['оглы', 'кызы']:
            return True
        if normal_form.endswith('вна') or normal_form.endswith('вич'):
            return True
        if normal_form in ['николаевна', 'ивановна', 'петровна', 'сергеевна', 'александровна', 'анатольевна', 'михайловна', 'владимировна']:
            return True

    common_names = {
        'иван', 'мария', 'анна', 'олег', 'александр', 'екатерина', 'андрей',
        'наталья', 'николай', 'ольга', 'виктор', 'людмила', 'сергей', 'екатерина',
        'алексей', 'дмитрий', 'татьяна', 'марина', 'евгений', 'людмила', 'лукиан'
    }
    if normal_form in common_names:
        return True

    return False

def extract_names_with_natasha(text):
    full_text = ' '.join(text) if isinstance(text, list) else text
    doc = Doc(full_text)

    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)

    names = set()
    for span in doc.spans:
        if span.type == PER:
            words = span.text.split()
            for word in words:
                if is_name_or_surname_or_patronymic(word):
                    names.add(word)

    for token in doc.tokens:
        word = token.text
        if is_name_or_surname_or_patronymic(word):
            names.add(word)

    return list(names)

def process_json(input_json):
    output_json = {}
    for class_name, class_data in input_json.items():
        output_json[class_name] = {"messages": []}
        for msg in class_data.get("messages", []):
            text_data = msg.get("text", [])
            flat_text = []
            for sublist in text_data:
                if isinstance(sublist, list):
                    flat_text.extend(sublist)
                else:
                    flat_text.append(sublist)

            extracted_names = extract_names_with_natasha(flat_text)

            new_msg = {
                "text": text_data,
                "names": extracted_names
            }
            output_json[class_name]["messages"].append(new_msg)

    return output_json

with open('data/prepared/normalized_texts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

result = process_json(data)

with open('data/prepared/normalized_texts_with_names.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Обработка завершена. Результат сохранён в output.json")

