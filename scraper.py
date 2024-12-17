import requests
from bs4 import BeautifulSoup
from database import get_db_session
from models import Word

BASE_URL = "https://ozhegov.slovaronline.com"

def scrape_words():
    session = get_db_session()
    url = f"{BASE_URL}/search"
    page = 1
    while True:
        response = requests.get(f"{url}?page={page}")
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, "html.parser")
        words = soup.find_all("div", class_="word-entry")
        if not words:
            break
        for word_entry in words:
            word_text = word_entry.find("a").text.strip()
            length = len(word)
            syllables = count_syllables(word_text)
            is_rare = is_word_rare(word_text)
            db_word = Word(word=word_text, length=length, syllables=syllables, is_rare=is_rare)
            session.add(db_word)
        session.commit()
        page += 1
    session.close()

def count_syllables(word):
    vowels = "аеёиоуыэюя"
    return sum(1 for char in word if char in vowels)

def is_word_rare(word):
    rare_letters = "фщцчъ"
    return "".join(set(word) & set(rare_letters))

if __name__ == "__main__":
    scrape_words()
