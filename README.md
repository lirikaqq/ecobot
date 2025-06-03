# 🌿 EcoBot Тиффа - ваш экогид в Telegram

<div align="center">
  <img src="https://via.placeholder.com/800x400/20B2AA/FFFFFF?text=EcoBot+Тиффа" alt="EcoBot Preview" width="600">
  
  [![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
  [![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://core.telegram.org/bots)
  [![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
</div>

## 📌 О проекте

EcoBot Тиффа - это интеллектуальный помощник для экологичного образа жизни, который предоставляет:

- 🌱 Актуальные экологические новости
- 🛍️ Каталог магазинов эко-товаров
- 🌦️ Персонализированную экологическую статистику
- 📊 Полезные эко-советы

## 🚀 Возможности

| Функция | Описание |
|---------|----------|
| 📰 Новости | Автоматический сбор статей об экологии с RBC Life |
| 🏪 Магазины | База 50+ экомагазинов в 15 городах России |
| 🌍 Экологическая карта | Визуализация данных о качестве воздуха |
| 💬 Обратная связь | Система сбора отзывов пользователей |

## 🛠 Технологии

```python
# Основной стек технологий
- Python 3.9+
- python-telegram-bot 13.7
- BeautifulSoup4 4.11.1
- Pillow 9.2.0
- Requests 2.28.1
⚙️ Установка
Клонируйте репозиторий:

bash
git clone https://github.com/ваш-логин/ecobot.git
cd ecobot
Установите зависимости:

bash
pip install -r requirements.txt
Настройте конфигурацию:

bash
mv config.example.py config.py
# Отредактируйте config.py
Запустите бота:

bash
python bot.py


📂 Структура проекта
ecobot/
├── bot.py                 # Основной модуль бота
├── config.py              # Конфигурация
├── requirements.txt       # Зависимости
├── article_parser.py      # Парсер новостей
├── image_downloader.py    # Загрузчик изображений
├── location_service.py    # Поиск магазинов
├── weather.py             # Погодная статистика
├── data/                  # Данные
│   ├── shops.json         # База магазинов
│   └── state.json         # Состояние бота
└── assets/                # Ресурсы
    ├── images/            # Изображения
    └── fonts/             # Шрифты
