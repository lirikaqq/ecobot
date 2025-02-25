import requests
from bs4 import BeautifulSoup

def download_image(url):
    try:
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')

        # Найти элемент <picture>
        picture_tag = soup.find('picture', class_='article-image-img')
        if picture_tag:
            # Попробуем найти первый доступный srcset или src
            image_url = None
            source_tags = picture_tag.find_all('source')
            for source in source_tags:
                if 'srcset' in source.attrs:
                    image_url = source['srcset'].split()[0]  # Берем первый URL из srcset
                    break

            if not image_url:
                img_tag = picture_tag.find('img')
                if img_tag and 'src' in img_tag.attrs:
                    image_url = img_tag['src']

            if image_url and not image_url.startswith('http'):
                image_url = 'https://www.rbc.ru' + image_url
            return image_url

    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")
    return None










