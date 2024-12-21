import requests
from bs4 import BeautifulSoup
import time
import logging
from database import get_db_session
from models import Word

BASE_URL = "https://ozhegov.slovaronline.com/articles"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}
OUTPUT_FILE = "words.txt"

def get_words_from_page(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Ошибка при загрузке страницы {url}: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    words = set()

    for block in soup.find_all("div", class_="article-link"):
        for link in block.find_all("a", title=True):
            word = link.get_text(strip=True) 
            if word: 
                words.add(word)

    return list(words)

def get_words_for_letter(letter):
    page = 1
    words = []

    while True:
        url = f"{BASE_URL}/{letter}/page-{page}"
        print(f"Парсим страницу: {url}")
        page_words = get_words_from_page(url)

        if not page_words:
            print(f"Страница {page} для буквы '{letter}' пуста. Переход к следующей букве.")
            break

        words.extend(page_words)
        print(f"Найдено слов: {len(page_words)} на странице {page} для буквы '{letter}'")
        page += 1
        time.sleep(1)

    return words

def main():
    alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    all_words = set()

    for letter in alphabet:
        print(f"Начинаем парсинг слов для буквы '{letter}'")
        letter_words = get_words_for_letter(letter)
        all_words.update(letter_words)

        print(f"Для буквы '{letter}' собрано {len(letter_words)} слов.\n")

    #сохраняем слова в файл
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        for word in sorted(all_words):
            file.write(word + "\n")

    print(f"Все слова сохранены в файл '{OUTPUT_FILE}'. Общее количество слов: {len(all_words)}")

def scrape_words():
    logging.info("here")
    session = get_db_session()
    for word_text in open("words.txt"):
        word_text = word_text.strip()
        length = len(word_text)
        syllables = count_syllables(word_text)
        is_rare = is_word_rare(word_text)
        db_word = Word(text=word_text, length=length, syllables=syllables, is_rare=is_rare)
        session.add(db_word)

    session.commit()
    logging.info("here1")
    session.close()

def count_syllables(word):
    vowels = "аеёиоуыэюя"
    return sum(1 for char in word if char in vowels)

def is_word_rare(word):
    rare_letters = "фщцчъ"
    return len("".join(set(word) & set(rare_letters))) != 0

if __name__ == "__main__":
    main()
    scrape_words()
