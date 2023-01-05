from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

btn_create_schedule = KeyboardButton(text='/Создать_расписание')

reply_key_board = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

btn_mon = InlineKeyboardButton(text='Понедельник', callback_data='Monday')
btn_tue = InlineKeyboardButton(text='Вторник', callback_data='Tuesday')
btn_wed = InlineKeyboardButton(text='Среда', callback_data='Wednesday')
btn_thu = InlineKeyboardButton(text='Четверг', callback_data='Thursday')
btn_fri = InlineKeyboardButton(text='Пятница', callback_data='Friday')

days_key_board = InlineKeyboardMarkup()
days_key_board.add(btn_mon, btn_tue, btn_wed, btn_thu, btn_fri)

btn_full = InlineKeyboardButton(text='9:00 - 18:30', callback_data='full')
btn_first_half = InlineKeyboardButton(text='9:00 - 14:00', callback_data='first_half')
btn_second_half = InlineKeyboardButton(text='14:00 - 18:30', callback_data='second_half')
btn_first_middle = InlineKeyboardButton(text='10:00 - 16:00', callback_data='first_middle')
btn_second_middle = InlineKeyboardButton(text='12:00 - 18:00', callback_data='second_middle')

btn_back = InlineKeyboardButton(text='Назад', callback_data='Back')
