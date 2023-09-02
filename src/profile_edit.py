from telebot import types
from src.keyboards import main_menu_kb


def edit_name(message, users, db, bot):
    # Сохраняем имя
    chat_id = message.chat.id
    name = message.text
    users[chat_id] = name

    # Запрашиваем фамилию
    bot.send_message(chat_id, 'Введите вашу фамилию:')
    bot.register_next_step_handler(message, lambda messege: edit_surname(messege, users, db, bot))


def edit_surname(message, users, db, bot):
    # Добавляем фамилию
    chat_id = message.chat.id
    surname = message.text
    users[chat_id]['surname'] = surname

    # Запрашиваем почту
    bot.send_message(chat_id, 'Введите вашу почту:')
    bot.register_next_step_handler(message, lambda messege: edit_email(messege, users, db, bot))


def edit_email(message, users, db, bot):
    chat_id = message.chat.id
    email = message.text

    # Сохраняем почту
    users[chat_id]['email'] = email
    user_info = users[chat_id]
    bot.send_message(chat_id, 'Введите ваш возраст:', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, lambda messege: edit_age(messege, users, db, bot))


def edit_age(message, users, db, bot):
    chat_id = message.chat.id
    age = message.text
    # Сохраняем возраст
    users[chat_id]['age'] = age

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("1 тип"), types.KeyboardButton("2 тип"))
    bot.send_message(chat_id, 'Выберете ваш тип диабета:', reply_markup=markup)
    bot.register_next_step_handler(message, lambda messege: edit_type_diabetes(messege, users, db, bot))


def edit_type_diabetes(message, users, db, bot):
    chat_id = message.chat.id
    type_diabetes = message.text
    # Сохраняем возраст
    users[chat_id]['type_diabetes'] = type_diabetes
    bot.send_message(chat_id, 'Введите ваш город:', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, lambda messege: edit_place(messege, users, db, bot))


def edit_place(message, users, db, bot):
    chat_id = message.chat.id
    place = message.text
    # Сохраняем возраст
    users[chat_id]['type_place'] = place
    bot.send_message(chat_id, 'Введите ваш контактный номер:')
    bot.register_next_step_handler(message, lambda messege: edit_number(messege, users, db, bot))


def edit_number(message, users, db, bot):
    chat_id = message.chat.id
    number = message.text
    # Сохраняем возраст
    users[chat_id]['number'] = number
    #db.insert_user(user_info['name'], user_info['surname'], user_info['email'])
    bot.send_message(chat_id, 'Данные сохранены')
    main_menu_kb(message, types.ReplyKeyboardMarkup(resize_keyboard=True), bot)


