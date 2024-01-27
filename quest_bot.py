import json
import telebot
from quest_bot.info1 import start, again, locations
from telebot import types

TOKEN = input("Введите токен:")
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
    bot.send_message(message.chat.id, locations['cave']['message'])
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    button_left = types.KeyboardButton(text=locations['cave']['choice1'])
    button_right = types.KeyboardButton(text=locations['cave']['choice2'])
    keyboard.add(button_left,button_right)
    bot.send_photo(message.chat.id, open('bats.jpg', 'rb'))
    bot.send_message(message.chat.id, "Выберите направление:", reply_markup=keyboard)
@bot.message_handler(func=lambda message: True)
def handle_choices(message):
    user_dict = load_user_data(str(message.chat.id))

    if message.text ==locations['cave']['choice1']:
        user_dict[str(message.chat.id)]['first_question']=message.text
        save_user_data(user_dict)
        bot.send_message(message.chat.id, locations['apple_tree']['message'])
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        button_eat = types.KeyboardButton(text=locations['apple_tree']['choice1'])
        button_not_eat = types.KeyboardButton(text=locations['apple_tree']['choice2'])
        keyboard.add(button_eat, button_not_eat)
        bot.send_photo(message.chat.id, open('apple_tree1.jpg', 'rb'))
        return bot.send_message(message.chat.id, "Что будешь делать?", reply_markup=keyboard)
    elif message.text == locations['cave']['choice2']:
        user_dict[str(message.chat.id)]['first_question'] = message.text
        save_user_data(user_dict)
        bot.send_message(message.chat.id, locations['sea']['message'])
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        button_swim = types.KeyboardButton(text=locations['sea']['choice1'])
        button_not_swim = types.KeyboardButton(text=locations['sea']['choice2'])
        keyboard.add(button_swim, button_not_swim)
        bot.send_photo(message.chat.id, open('beach.jpg', 'rb'))
        return bot.send_message(message.chat.id, "Что будешь делать?", reply_markup=keyboard)
    elif message.text == locations['apple_tree']['choice1']:
        user_dict[str(message.chat.id)]['second_question']=message.text
        user_dict[str(message.chat.id)]['result']=locations['results']['lose2']
        save_user_data(user_dict)
        bot.send_photo(message.chat.id, open('apple.jpg', 'rb'))
        bot.send_message(message.chat.id,locations['results']['lose2'])
        bot.send_photo(message.chat.id, open('goat.jpg', 'rb'))
        bot.send_message(message.chat.id, again)
    elif message.text == locations['sea']['choice1']:
        user_dict[str(message.chat.id)]['second_question']=message.text
        user_dict[str(message.chat.id)]['result']=locations['results']['lose1']
        save_user_data(user_dict)
        bot.send_message(message.chat.id, locations['results']['lose1'])
        bot.send_photo(message.chat.id, open('sharks1.jpg', 'rb'))
        bot.send_message(message.chat.id, again)
    elif message.text == locations['apple_tree']['choice2']:
        user_dict[str(message.chat.id)]['second_question']=message.text
        user_dict[str(message.chat.id)]['result']=locations['results']['win2']
        save_user_data(user_dict)
        bot.send_message(message.chat.id, locations['results']['win2'])
        bot.send_photo(message.chat.id, open('apple_tree4.jpg', 'rb'))
        bot.send_message(message.chat.id, again)
    elif message.text == locations['sea']['choice2']:
        user_dict[str(message.chat.id)]['second_question']=message.text
        user_dict[str(message.chat.id)]['result']=locations['results']['win1']
        save_user_data(user_dict)
        bot.send_message(message.chat.id,locations['results']['win1'])
        bot.send_photo(message.chat.id, open('fire3.jpg', 'rb'))
        bot.send_photo(message.chat.id, open('ship5.jpg', 'rb'))
        bot.send_message(message.chat.id, again)
    else:
        bot.send_message(message.chat.id, f"Я не понимаю. Начните игру заново и используйте клавиши для выбора действий")
        bot.send_message(message.chat.id, again)

bot.polling()