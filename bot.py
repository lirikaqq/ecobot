import json
import os
from telebot import TeleBot, types
from article_parser import extract_articles, get_article_text
from image_downloader import download_image
from location_service import get_random_eco_shops, get_eco_shops_message
from weather import generate_weather_image

bot = TeleBot(token='8073573771:AAH5nfUUvJp40dJBg2PsKyvW9yv5wzQIWik')

last_article_message = {}
last_list_message = {}
user_states = {}

STATE_FILE = 'bot_state.json'

def save_state():
    state = {
        'last_article_message': last_article_message,
        'last_list_message': last_list_message,
        'user_states': user_states
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def load_state():
    global last_article_message, last_list_message, user_states
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
            last_article_message = state.get('last_article_message', {})
            last_list_message = state.get('last_list_message', {})
            user_states = state.get('user_states', {})

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Да!🔅"))
    bot.send_message(
        message.chat.id,
        "Привет! Я ЭкоБот-Тиффа 🌱\n\n"
        "Я помогу тебе узнать эко-новости, найти магазины с чистыми продуктами и посмотреть эко-статистику в твоем районе.\n\n"
        "Начнем?",
        reply_markup=markup
    )

@bot.message_handler(content_types=['text'])
def get_message(message):
    user_id = message.from_user.id

    if message.text == 'Да!🔅':
        show_main_menu(message)

    elif message.text == 'Назад в меню':
        user_states.pop(user_id, None)
        return_to_menu(message)

    elif message.text == 'Новости об экологических событиях':
        articles = extract_articles('https://www.rbc.ru/life/tag/ecology')
        if not articles:
            bot.send_message(user_id, "Статьи не найдены.")
            return
        markup = types.InlineKeyboardMarkup()
        for article in articles:
            markup.add(types.InlineKeyboardButton(text=article['title'], callback_data=article['url']))
        sent_message = bot.send_message(user_id, 'Выберите статью:', reply_markup=markup)
        last_list_message[user_id] = sent_message.message_id

    elif message.text == 'Магазины с экологически чистыми продуктами':
        user_states[user_id] = 'waiting_for_city'
        bot.send_message(user_id, "Напишите название вашего города.")

    elif message.text == 'Эко-статистика по твоему городу':
        user_states[user_id] = 'waiting_for_stats_city'
        bot.send_message(user_id, "Введите ваш город для получения эко-статистики.")

    elif message.text == 'Оставить отзыв':
        ask_for_feedback(message)

    elif user_states.get(user_id) == 'waiting_for_city':
        handle_city_input(message)

    elif user_states.get(user_id) == 'waiting_for_stats_city':
        handle_stats_city_input(message)

    elif user_states.get(user_id) == 'waiting_for_feedback':
        handle_feedback(message)

@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    article_url = call.data
    article_text = get_article_text(article_url)
    image_url = download_image(article_url)

    caption = article_text
    if len(article_text) > 1024:
        caption = article_text[:1024]
        last_punct = max(caption.rfind("."), caption.rfind("!"), caption.rfind("?"))
        if last_punct != -1:
            caption = caption[:last_punct + 1]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Назад в меню'))

    if call.message.chat.id in last_article_message:
        bot.delete_message(call.message.chat.id, last_article_message[call.message.chat.id])

    if image_url:
        sent_message = bot.send_photo(call.message.chat.id, image_url, caption=caption, parse_mode='HTML', reply_markup=markup)
    else:
        sent_message = bot.send_message(call.message.chat.id, article_text, parse_mode='HTML', reply_markup=markup)

    last_article_message[call.message.chat.id] = sent_message.message_id

def handle_city_input(message):
    user_id = message.from_user.id
    city = message.text
    shops = get_random_eco_shops(city)
    reply = get_eco_shops_message(shops)
    bot.send_message(user_id, reply, parse_mode='Markdown', disable_web_page_preview=True)
    return_to_menu(message)

def handle_stats_city_input(message):
    user_id = message.from_user.id
    city = message.text

    generating_message = bot.send_message(user_id, "Генерирую изображение...")

    image_path = generate_weather_image(city)
    if image_path and os.path.exists(image_path):
        with open(image_path, 'rb') as photo:
            bot.send_photo(user_id, photo, caption="Вот эко-статистика по вашему городу.", reply_markup=get_main_menu_markup())
    else:
        bot.send_message(user_id, "Не удалось получить данные. Убедитесь, что город указан корректно.", reply_markup=get_main_menu_markup())

    bot.delete_message(user_id, generating_message.message_id)

    return_to_menu(message)

def ask_for_feedback(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Пожалуйста, напишите ваш отзыв:")
    user_states[user_id] = 'waiting_for_feedback'

def handle_feedback(message):
    user_id = message.from_user.id
    feedback = message.text
    save_feedback(user_id, feedback)
    bot.send_message(user_id, "Спасибо за ваш отзыв!❤️")
    return_to_menu(message)

def save_feedback(user_id, feedback):
    with open('feedback.txt', 'a', encoding='utf-8') as f:
        f.write(f"User ID: {user_id}\nFeedback: {feedback}\n\n")

def show_main_menu(message):
    markup = get_main_menu_markup()
    bot.send_message(message.chat.id, 'Выберите опцию из меню:', reply_markup=markup)

def return_to_menu(message):
    if message.from_user.id in last_list_message:
        try:
            bot.delete_message(message.chat.id, last_list_message[message.from_user.id])
        except:
            pass
    if message.from_user.id in last_article_message:
        try:
            bot.delete_message(message.chat.id, last_article_message[message.from_user.id])
        except:
            pass
    show_main_menu(message)

def get_main_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton('Магазины с экологически чистыми продуктами'),
        types.KeyboardButton('Новости об экологических событиях'),
        types.KeyboardButton('Эко-статистика по твоему городу'),
        types.KeyboardButton('Оставить отзыв')
    )
    return markup

def main():
    load_state()
    try:
        bot.infinity_polling()
    finally:
        save_state()

if __name__ == '__main__':
    main()
