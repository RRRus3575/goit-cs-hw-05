import requests
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import threading
import time

# Функція для завантаження тексту з URL
def fetch_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Не вдалося отримати дані з {url}, код статусу: {response.status_code}")

# Map етап: розбивка тексту на слова
def map_words(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return words

# Reduce етап: підрахунок кількості слів
def reduce_word_counts(word_list):
    return Counter(word_list)

# Візуалізація топ N слів
def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)
    
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Частота')
    plt.ylabel('Слова')
    plt.title(f'Топ {top_n} найчастіше вживаних слів')
    plt.show()

# Функція для заглушки
def loading_message():
    while not finished:
        print("Йде завантаження...", end="\r")
        time.sleep(0.5)

# Головна функція для запуску MapReduce і візуалізації результатів
def main():
    global finished
    finished = False
    
    url = input("Введіть посилання для аналізу: ")
    
    loading_thread = threading.Thread(target=loading_message)
    loading_thread.start()
    
    try:
        text = fetch_text(url)
        
        with ThreadPoolExecutor() as executor:
            word_lists = executor.submit(map_words, text).result()

        word_counts = reduce_word_counts(word_lists)

        visualize_top_words(word_counts)
    
    finally:
        finished = True
        loading_thread.join()


if __name__ == "__main__":
    main()


# Приклад URL з текстом
url = 'https://www.gutenberg.org/files/1342/1342-0.txt'