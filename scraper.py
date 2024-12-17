import logging
import requests
from bs4 import BeautifulSoup
from database import get_db_session
from models import Word

BASE_URL = "https://ozhegov.slovaronline.com"
WORDS_FILE = "words.txt"

def scrape_words():
    logging.info("Начинаем парсинг сайта...")
    words = get_all_words_from_site()
    save_words_to_file(words, WORDS_FILE)

    session = get_db_session()

    for word_text in words:
        word_text = word_text.strip()
        length = len(word_text)
        syllables = count_syllables(word_text)
        is_rare = is_word_rare(word_text)
        db_word = Word(text=word_text, length=length, syllables=syllables, is_rare=is_rare)
        session.add(db_word)

    session.commit()
    logging.info("Все слова добавлены в базу данных.")
    session.close()

def get_all_words_from_site():

    alphabet_links = get_alphabet_links()
    all_words = set()

    for link in alphabet_links:
        logging.info(f"Обрабатываем страницу: {link}")
        words = get_words_from_page(link)
        all_words.update(words)

    return list(all_words)

def get_alphabet_links():

    response = requests.get(BASE_URL)
    if response.status_code != 200:
        logging.error(f"Ошибка при доступе")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    alphabet_section = soup.find("div", class_="list-links")
    if alphabet_section:
        for a_tag in alphabet_section.find_all("a", href=True):
            links.append(BASE_URL + a_tag["href"])
    return links

def get_words_from_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Ошибка при доступе")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    words = []

    word_tags = soup.find_all("a", class_="word")
    for word_tag in word_tags:
        word = word_tag.text.strip()
        if word:
            words.append(word)
    return words

def save_words_to_file(words, filename):
 
    with open(filename, "w", encoding="utf-8") as file:
        for word in words:
            file.write(word + "\n")
    logging.info(f"Слова сохранены в файл words.txt.")

def count_syllables(word):
    vowels = "аеёиоуыэюя"
    return sum(1 for char in word if char in vowels)

def is_word_rare(word):
    rare_letters = "фщцчъ"
    return len("".join(set(word) & set(rare_letters))) != 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scrape_words()
