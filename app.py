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


def save_results(results):
    with open("results.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "sentiment", "score"])
        writer.writeheader()
        writer.writerows(results)


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
    "Мне очень понравился этот продукт",
    "Замечательное качество и быстрая доставка",
    "Очень хороший магазин",
    "Я доволен покупкой",
    "Прекрасный сервис и поддержка",
    "Очень удобное приложение",
    "Все работает идеально",
    "Отличная работа разработчиков",
    "Я люблю этот сервис",

    "Сервис работает нормально",
    "В целом неплохо",
    "Продукт обычный",
    "Работает как и ожидалось",
    "Нормальный результат",
    "Среднее качество",
    "Ничего особенного",
    "Можно пользоваться",
    "Иногда работает медленно",
    "В целом нормально",

    "Очень плохой сервис",
    "Это был ужасный опыт",
    "Приложение работает отвратительно",
    "Я крайне недоволен",
    "Поддержка совершенно не помогает",
    "Ужасное качество продукта",
    "Очень разочарован покупкой",
    "Все работает плохо",
    "Это худший сервис",
    "Я ненавижу это приложение"
]

results = []

for text in texts:
    result = analyze_sentiment(text)
    print(result)

    results.append({
        "text": result["text"],
        "sentiment": result["sentiment"],
        "score": result["score"]
    })

save_results(results)