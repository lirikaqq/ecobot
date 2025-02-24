import requests
from bs4 import BeautifulSoup

# Функция для получения текста статьи
def get_article_text(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')

    # Найти все параграфы с классом 'paragraph'
    paragraphs = soup.find_all('p', class_='paragraph')

    # Извлечь текст из каждого параграфа
    article_text = "\n\n".join([para.get_text(separator=' ', strip=True) for para in paragraphs])

    # Выделяем первый абзац жирным шрифтом
    if paragraphs:
        first_paragraph = f"<b>{paragraphs[0].get_text(separator=' ', strip=True)}</b>"
        remaining_text = "\n\n".join([para.get_text(separator=' ', strip=True) for para in paragraphs[1:]])
        article_text = f"{first_paragraph}\n\n{remaining_text}"

    article_text = article_text.replace("Читать РБК Life в Telegram", "").strip()

    return article_text


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

    return articles[:5]

