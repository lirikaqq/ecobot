from telebot import TeleBot, types
from article_parser import extract_articles, get_article_text
from image_downloader import download_image

# Инициализация бота
bot = TeleBot(token='')

# Переменные для хранения последних отправленных сообщений
last_article_message = {}
last_list_message = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Да!🔅")
    markup.add(btn1)
    bot.send_message(
        message.from_user.id,
        "Привет! Я ЭкоБот-Тиффа, я увлекаюсь экологией и берегу окружающую среду 😇\n\n"
        "**Этот бот находится в стадии разработки, поэтому могут быть неточности. "
        "Новостную информацию мы получаем с открытого пространства [РБК](https://www.rbc.ru/life/tag/ecology).**\n\n"
        "Начнём вместе сохранять нашу планету?",
        parse_mode='Markdown',
        reply_markup=markup
    )

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_message(message):
    if message.text == 'Да!🔅':
        show_main_menu(message)

    elif message.text == 'Назад в меню':
        return_to_menu(message)

    elif message.text == 'Новости об экологических событиях':
        articles = extract_articles('https://www.rbc.ru/life/tag/ecology')  # URL страницы с несколькими статьями

        if not articles:
            bot.send_message(message.from_user.id, "Статьи не найдены.")
            return

        # Создаем клавиатуру с выбором статей
        markup = types.InlineKeyboardMarkup()
        for article in articles:
            markup.add(types.InlineKeyboardButton(text=article['title'], callback_data=article['url']))

        sent_message = bot.send_message(message.from_user.id, 'Выберите статью:', reply_markup=markup)

        # Сохраняем ID отправленного сообщения с перечнем статей
        last_list_message[message.from_user.id] = sent_message.message_id

# Обработчик нажатий на inline-кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    article_url = call.data
    article_text = get_article_text(article_url)
    image_url = download_image(article_url)

    # Обрезаем текст до 1024 символов, не обрывая предложение
    if len(article_text) > 1024:
        caption = article_text[:1024]
        last_punctuation_index = max(
            caption.rfind("."),
            caption.rfind("!"),
            caption.rfind("?")
        )
        if last_punctuation_index != -1:
            caption = caption[:last_punctuation_index + 1]
    else:
        caption = article_text

    # Создаем клавиатуру с кнопкой "Назад в меню"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = types.KeyboardButton('Назад в меню')
    markup.add(back_button)

    # Удаляем предыдущее сообщение, если оно существует
    if call.message.chat.id in last_article_message:
        bot.delete_message(call.message.chat.id, last_article_message[call.message.chat.id])

    if image_url:
        sent_message = bot.send_photo(call.message.chat.id, image_url, caption=caption, parse_mode='HTML', reply_markup=markup)
    else:
        sent_message = bot.send_message(call.message.chat.id, article_text, parse_mode='HTML', reply_markup=markup)
        bot.send_message(call.message.chat.id, "К сожалению, изображение не найдено.", reply_markup=markup)

    # Сохраняем ID отправленного сообщения
    last_article_message[call.message.chat.id] = sent_message.message_id

def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.KeyboardButton('Магазины с экологически чистыми продуктами')
    btn3 = types.KeyboardButton('Новости об экологических событиях')
    btn4 = types.KeyboardButton('Эко-статистика по твоему городу')
    markup.add(btn2, btn3, btn4)
    bot.send_message(message.from_user.id, 'С чего начнём❓', reply_markup=markup)

def return_to_menu(message):
    # Удаляем последние сообщения с перечнем статей и статьей
    if message.from_user.id in last_list_message:
        bot.delete_message(message.chat.id, last_list_message[message.from_user.id])
    if message.from_user.id in last_article_message:
        bot.delete_message(message.chat.id, last_article_message[message.from_user.id])

    show_main_menu(message)

def main():
    # Запускаем бота
    bot.infinity_polling()

if __name__ == '__main__':
    main()
