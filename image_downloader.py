import requests
from bs4 import BeautifulSoup

def download_image(url):
    try:
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')

        # Найти первое изображение в статье
        image_tag = soup.find('img', class_='article__main-image__image')
        if image_tag and 'src' in image_tag.attrs:
            image_url = image_tag['src']
            # Проверяем, что ссылка является полной
            if not image_url.startswith('http'):
                image_url = 'https://www.rbc.ru' + image_url
            return image_url
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")
    return None
