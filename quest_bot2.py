import json
import telebot
from info import start, go, left_choice, right_choice, lose1, lose2, win1, win2, again
from telebot import types

TOKEN =input("Ведите токен для своего бота")
bot = telebot.TeleBot(TOKEN)

def save_user_data(result):
    with open("user_data.json", "r") as file:
        users_data = json.load(file)
    users_data.update(result)
    with open("user_data.json", "w") as file:
        json.dump(users_data, file, indent=4)

def load_user_data(user_id):
    with open("user_data.json", "r") as file:
        users_data=json.load(file)
        if str(user_id) in users_data.keys():
            return {str(user_id): users_data[str(user_id)]}
        else:
            return {str(user_id):{'first_question': None, 'second_question': None, 'result': None}}
def filter_start(message):
    password = '/start'
    return True

@bot.message_handler(commands=['start'], func=filter_start)
def say_start(message):
    bot.send_message(message.chat.id, start)

@bot.message_handler(commands=['go'])
def handle_go(message):
    bot.send_photo(message.chat.id, open('cave1.jpg', 'rb'))
    bot.send_message(message.chat.id, go)
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    button_right = types.KeyboardButton(text="Пожалуй-ка я пойду направо...")
    button_left = types.KeyboardButton(text="Лево мне больше нравится...")
    keyboard.add(button_right, button_left)
    bot.send_photo(message.chat.id, open('bats.jpg', 'rb'))
    bot.send_message(message.chat.id, "Выберите направление:", reply_markup=keyboard)
@bot.message_handler(func=lambda message: True)
def handle_choices(message):
    user_dict = load_user_data(str(message.chat.id))

    if message.text == "Лево мне больше нравится...":
        user_dict[str(message.chat.id)]['first_question']=message.text
        save_user_data(user_dict)
        bot.send_message(message.chat.id, left_choice)
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        button_eat = types.KeyboardButton(text="Я очень голоден, не могу удержаться...")
        button_not_eat = types.KeyboardButton(text="Потерплю до дома, хотя так хочется")
        keyboard.add(button_eat, button_not_eat)
        bot.send_photo(message.chat.id, open('apple_tree1.jpg', 'rb'))
        return bot.send_message(message.chat.id, "Что будешь делать?", reply_markup=keyboard)
    elif message.text == "Пожалуй-ка я пойду направо...":
        user_dict[str(message.chat.id)]['first_question'] = message.text
        save_user_data(user_dict)
        bot.send_message(message.chat.id, right_choice)
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        button_swim = types.KeyboardButton(text="Будь что будет, поплыву...")
        button_not_swim = types.KeyboardButton(text="Буду надеяться на лучшее, а лучше разведу огонь")
        keyboard.add(button_swim, button_not_swim)
        bot.send_photo(message.chat.id, open('beach.jpg', 'rb'))
        return bot.send_message(message.chat.id, "Что будешь делать?", reply_markup=keyboard)
    elif message.text == "Я очень голоден, не могу удержаться...":
        user_dict[str(message.chat.id)]['second_question']=message.text
        user_dict[str(message.chat.id)]['result']=lose2
        save_user_data(user_dict)
        bot.send_photo(message.chat.id, open('apple.jpg', 'rb'))
        bot.send_message(message.chat.id, lose2)
        bot.send_photo(message.chat.id, open('goat.jpg', 'rb'))
        bot.send_message(message.chat.id, again)
    elif message.text == "Будь что будет, поплыву...":
        user_dict[str(message.chat.id)]['second_question']=message.text
        user_dict[str(message.chat.id)]['result']=lose1
        save_user_data(user_dict)
        bot.send_message(message.chat.id, lose1)
        bot.send_photo(message.chat.id, open('sharks1.jpg', 'rb'))
        bot.send_message(message.chat.id, again)
    elif message.text == "Потерплю до дома, хотя так хочется":
        user_dict[str(message.chat.id)]['second_question']=message.text
        user_dict[str(message.chat.id)]['result']=win2
        save_user_data(user_dict)
        bot.send_message(message.chat.id, win2)
        bot.send_photo(message.chat.id, open('apple_tree4.jpg', 'rb'))
        bot.send_message(message.chat.id, again)
    elif message.text == "Буду надеяться на лучшее, а лучше разведу огонь":
        user_dict[str(message.chat.id)]['second_question']=message.text
        user_dict[str(message.chat.id)]['result']=win1
        save_user_data(user_dict)
        bot.send_message(message.chat.id, win1)
        bot.send_photo(message.chat.id, open('fire3.jpg', 'rb'))
        bot.send_photo(message.chat.id, open('ship5.jpg', 'rb'))
        bot.send_message(message.chat.id, again)
    else:
        bot.send_message(message.chat.id, f"Я не понимаю. Начните игру заново и используйте клавиши для выбора действий")
        bot.send_message(message.chat.id, again)

bot.polling()