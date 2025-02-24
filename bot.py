from telebot import TeleBot, types
from article_parser import extract_articles, get_article_text
from image_downloader import download_image

# Инициализация бота
bot = TeleBot(token='', parse_mode='html')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Да!🔅")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Привет я ЭкоБот-Наталья, я увлекаюсь экологией и берегу окружающую среду 😇 \nНачнём вместе сохранять нашу планету?", reply_markup=markup)

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_message(message):
    if message.text == 'Да!🔅':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn2 = types.KeyboardButton('Магазины с экологически чистыми продуктами')
        btn3 = types.KeyboardButton('Новости об экологических событиях')
        btn4 = types.KeyboardButton('Эко-статистика по твоему городу')
        markup.add(btn2, btn3, btn4)
        bot.send_message(message.from_user.id, 'С чего начнём❓', reply_markup=markup)

    elif message.text == 'Новости об экологических событиях':
        articles = extract_articles('https://www.rbc.ru/life/tag/ecology')  # URL страницы с несколькими статьями

        if not articles:
            bot.send_message(message.from_user.id, "Статьи не найдены.")
            return

        # Создаем клавиатуру с выбором статей
        markup = types.InlineKeyboardMarkup()
        for article in articles:
            markup.add(types.InlineKeyboardButton(text=article['title'], callback_data=article['url']))

        bot.send_message(message.from_user.id, 'Выберите статью:', reply_markup=markup)

# Обработчик нажатий на inline-кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    article_url = call.data
    article_text = get_article_text(article_url)
    image_url = download_image(article_url)

    if image_url:
        bot.send_photo(call.message.chat.id, image_url, caption=article_text)
    else:
        bot.send_message(call.message.chat.id, article_text)
        bot.send_message(call.message.chat.id, "К сожалению, изображение не найдено.")

def main():
    # Запускаем бота
    bot.infinity_polling()

if __name__ == '__main__':
    main()
