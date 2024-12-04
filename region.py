import telebot
import logging

BOT_TOKEN = 'token'  # Замените на свой токен
bot = telebot.TeleBot(BOT_TOKEN)

region_facts = {
    'Приморский край': [
        {"text": "Приморский край – единственный регион России, где обитает амурский тигр в дикой природе.//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////", "photo_path": "C:/Users/Evelina/PycharmProjects/bot3/photos/file_0.jpg"},
        {"text": "На территории края находится самый большой в России остров – Сахалин.", "photo_path": "C:/Users/Evelina/PycharmProjects/bot3/photos/file_0.jpg"},
        {"text": "В Приморье расположены уникальные природные объекты, такие как озеро Ханка и Сихотэ-Алинь.", "photo_path": "C:/Users/Evelina/PycharmProjects/bot3/photos/file_0.jpg"},
    ],
    'Хабаровск': [
        {"text": "Хабаровск – крупнейший город на Дальнем Востоке России.", "photo_path": "C:/Users/Evelina/PycharmProjects/bot3/photos/file_0.jpg"},
        {"text": "В Хабаровске находится единственный в России музей истории Дальнего Востока.", "photo_path": "C:/Users/Evelina/PycharmProjects/bot3/photos/file_0.jpg"},
        {"text": "Хабаровск расположен на слиянии рек Амур и Уссури.", "photo_path": "C:/Users/Evelina/PycharmProjects/bot3/photos/file_0.jpg"},
    ],
    'Кемеровская область': [
        {"text": "Кемеровская область – один из крупнейших угольных бассейнов в России.", "photo_path": "C:/Users/Evelina/PycharmProjects/bot3/photos/file_0.jpg"},
        {"text": "В Кемеровской области находится знаменитая гора Кузнецкий Алатау.", "photo_path": "C:/Users/Evelina/PycharmProjects/bot3/photos/file_0.jpg"},
        {"text": "Кемеровская область богата разнообразными природными ресурсами, включая леса и реки.", "photo_path": "C:/Users/Evelina/PycharmProjects/bot3/photos/file_0.jpg"},
    ],
}

user_state = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Приморский край', 'Хабаровск', 'Кемеровская область')
    bot.send_message(message.chat.id, "Выберите регион:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in region_facts)
def handle_region(message):
    chat_id = message.chat.id
    user_state[chat_id] = {'region': message.text, 'fact_index': 0}
    show_fact(message)

def show_fact(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)
    if not state:
        return

    region = state['region']
    fact_index = state['fact_index']
    facts = region_facts.get(region, [])
    if fact_index >= len(facts):
        bot.send_message(chat_id, "Больше фактов нет!")
        return

    fact = facts[fact_index]
    full_text = fact['text']
    short_text = full_text[:100] + "..." if len(full_text) > 100 else full_text

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    if len(full_text) > 100:
        markup.add(telebot.types.KeyboardButton("Читать дальше"))
    if fact_index + 1 < len(facts):
        markup.add(telebot.types.KeyboardButton("Следующий факт"))

    photo_path = fact.get('photo_path')
    try:
        if photo_path:
            with open(photo_path, 'rb') as photo:
                msg = bot.send_photo(chat_id, photo, caption=short_text, reply_markup=markup)
        else:
            msg = bot.send_message(chat_id, short_text, reply_markup=markup)
        user_state[chat_id]['msg_id'] = msg.message_id  #Save message ID for editing if needed in future
    except FileNotFoundError:
        bot.send_message(chat_id, f"Фотография не найдена: {photo_path}")
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка при отправке фото: {e}")


@bot.message_handler(func=lambda message: message.text == "Читать дальше")
def read_more(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)
    if state:
        region = state['region']
        fact_index = state['fact_index']
        facts = region_facts[region]
        full_text = facts[fact_index]['text']
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        if fact_index + 1 < len(facts):
            markup.add(telebot.types.KeyboardButton("Следующий факт"))
        bot.send_message(chat_id, full_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Следующий факт")
def next_fact(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)
    if state:
        state['fact_index'] += 1
        show_fact(message)

bot.infinity_polling()