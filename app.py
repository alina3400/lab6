import csv
import re
import pymorphy2
import pymorphy2_dicts_ru

morph = pymorphy2.MorphAnalyzer(
    path=pymorphy2_dicts_ru.get_path()
)

# загрузка словаря
dictionary = {}

with open("dictionary.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        dictionary[row["word"]] = int(row["score"])


def lemmatize(word):
    parsed = morph.parse(word)[0]
    return parsed.normal_form


def analyze_sentiment(text):
    words = re.findall(r'\w+', text.lower())

    score = 0
    found_words = []

    for word in words:
        lemma = lemmatize(word)

        if lemma in dictionary:
            score += dictionary[lemma]
            found_words.append(lemma)

    if score > 0:
        sentiment = "positive"
    elif score < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "text": text,
        "sentiment": sentiment,
        "score": score,
        "matched_words": found_words
    }

texts = [
    "Этот сервис просто отличный",
    "Это был ужасный опыт",
    "Сервис работает нормально",
    "Я очень люблю этот продукт"
]

for text in texts:
    result = analyze_sentiment(text)
    print(result)