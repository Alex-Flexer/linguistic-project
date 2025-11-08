import json
from collections import Counter, defaultdict
import os


def analyze_words_by_name(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    name_word_stats = defaultdict(Counter)

    for class_name, class_data in data.items():
        for message in class_data['messages']:
            text_segments = message['text']
            names = message['names']

            if names:
                all_words = []
                for segment in text_segments:
                    all_words.extend(segment)

                for name in names:
                    filtered_words = [word for word in all_words
                                      if word != name and len(word) > 1]
                    name_word_stats[name].update(filtered_words)

    sorted_stats = {}
    for name, word_counter in name_word_stats.items():
        sorted_words = sorted(word_counter.items(), key=lambda x: x[1], reverse=True)
        sorted_stats[name] = sorted_words

    return dict(sorted_stats)


def main():
    file_path = "data/prepared/normalized_texts_with_names.json"

    name_statistics = analyze_words_by_name(file_path)

    print("СТАТИСТИКА СЛОВ ПО ИМЕНАМ (от большего к меньшему)")

    for name, words_stats in name_statistics.items():
        print(f"\n{name.upper()}:")

        if words_stats:
            for i, (word, count) in enumerate(words_stats[:20], 1):
                print(f"  {i:2d}. {word:<15} - {count} раз")
        else:
            print("Нет данных о словах")

        print(f"Всего уникальных слов: {len(words_stats)}")
        total_occurrences = sum(count for _, count in words_stats)
        print(f"Всего употреблений слов: {total_occurrences}")

    output_file = "name_word_statistics.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(name_statistics, f, ensure_ascii=False, indent=2)

    print(f"\nПолная статистика сохранена в файл: {output_file}")

    print(f"\nСВОДНАЯ ИНФОРМАЦИЯ:")
    print(f"Всего имен: {len(name_statistics)}")

    names_by_word_count = sorted(name_statistics.items(),
                                 key=lambda x: len(x[1]),
                                 reverse=True)

    print(f"\nТоп-10 имен с наибольшим количеством уникальных слов:")
    for i, (name, words_stats) in enumerate(names_by_word_count[:10], 1):
        print(f"  {i:2d}. {name:<15} - {len(words_stats)} уникальных слов")


if __name__ == "__main__":
    main()
