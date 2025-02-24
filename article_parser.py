import requests
from bs4 import BeautifulSoup

# Функция для извлечения заголовков и ссылок со страницы
def extract_articles(page_url):
    response = requests.get(page_url).text
    soup = BeautifulSoup(response, 'html.parser')

    # Найти все статьи на странице
    articles = []
    for item in soup.find_all('a', class_='info-block-title', href=True):
        title = item.get_text(strip=True)
        link = item['href']
        # Проверяем, что ссылка является полной
        if not link.startswith('http'):
            link = 'https://www.rbc.ru' + link
        articles.append({"title": title, "url": link})

    return articles

# Пример использования
page_url = 'https://www.rbc.ru/life/tag/ecology'  # URL страницы с несколькими статьями
articles = extract_articles(page_url)

for article in articles:
    print(f"Заголовок: {article['title']}")
    print(f"Ссылка: {article['url']}")
    print()
    