import pandas as pd
import numpy as np
import states
import config

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import TOKEN, callback_words, FULL_TIME, FIRST_HALF, SECOND_HALF, FIRST_MIDDLE, SECOND_MIDDLE, DAYS,\
    FILL_HOURS

from messages import MESSAGES
import btns

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
employees = pd.DataFrame(pd.read_csv('employees.csv', encoding='utf-8', delimiter=';', index_col=0))
WEEK = str


############################################################################################################


def create_schedule(week: str):
    """
    This function creates an empty schedule for the week. And saves it in .csv format.
    :param week: str
    """
    global WEEK
    WEEK = week
    data = np.full((30, 5), np.nan)
    schedule_week = pd.DataFrame(columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], data=data)
    with open(f'Расписание на {week}.csv', 'w', encoding='utf-8') as f:
        schedule_week.to_csv(f, sep=';', encoding='utf-8')


def fill_schedule(bl: int, al: int, day: str, week: str):
    """
    This function fills the schedule based on the number of children for each day of the week.
    That is, it creates time slots based on the rule that 1 teacher is needed for 4 children
    :param bl: int - number of children before lunch
    :param al: int - number of children after lunch
    :param day: str
    :param week: str
    """
    day = DAYS[day]
    specs_bl = int(np.ceil(bl / 4))
    specs_al = int(np.ceil(al / 4))
    specs_full = min(specs_bl, specs_al)
    hours = []
    try:
        schedule = pd.read_csv(f'Расписание на {week}.csv', delimiter=';', index_col=0)
        hours.extend((specs_full * FULL_TIME).split(',')[:-1])
        hours.extend((specs_bl * FIRST_HALF).split(',')[:-1])
        hours.extend((specs_al * SECOND_HALF).split(',')[:-1])
        diff = abs(len(schedule) - len(hours))
        hours.extend([np.nan for _ in range(diff)])
        if all(schedule[day]):
            schedule.loc[:, day] = hours
        else:
            pass
        schedule.to_csv(f'Расписание на {week}.csv', sep=';', encoding='utf-8')
        return schedule
    except Exception:
        pass


def hours_buttons(hours: list):
    """
    This function creates InlineKeyboardMarkup, which fills by buttons of time slots
    :param hours: list
    :return: InlineKeyboardMarkup
    """
    vacancy_key_board = InlineKeyboardMarkup()
    for hour in hours:
        if hour == FULL_TIME[:-1]:
            vacancy_key_board.add(btns.btn_full)
        elif hour == FIRST_HALF[:-1]:
            vacancy_key_board.add(btns.btn_first_half)
        elif hour == SECOND_HALF[:-1]:
            vacancy_key_board.add(btns.btn_second_half)
        elif hour == FIRST_MIDDLE[:-1]:
            vacancy_key_board.add(btns.btn_first_middle)
        elif hour == SECOND_MIDDLE[:-1]:
            vacancy_key_board.add(btns.btn_second_middle)
    vacancy_key_board.add(btns.btn_back)
    return vacancy_key_board


def check_day(day: str):
    """
    This function checks how many time slots are vacancy on that day
    :param day: str
    :return: list
    """
    global WEEK
    hours = []
    day = day.capitalize()
    try:
        schedule = pd.read_csv(f'Расписание на {WEEK}.csv', delimiter=';')
        for h in schedule.loc[:, day]:
            if type(h) == float:
                break
            if h[0].isalpha():
                pass
            if not h.isalpha():
                hours.append(h)
            else:
                pass
        return list(set(hours))
    except Exception:
        pass


def fill_slot(day: str, user_id: str, hours: str):
    """
    This function fills the slots with the names of workers who have decided to take this slot for themselves.
    :param day: str
    :param user_id: str
    :param hours: str
    :return:
    """
    global WEEK
    try:
        week = pd.read_csv(f'Расписание на {WEEK}.csv', delimiter=';', index_col=0)
        employee_name = employees['name'].loc[employees['tg_id'] == user_id].values[0]
        if any(i.startswith(employee_name) for i in week[day].dropna()):
            return False
        for index, fill_hours in enumerate(week[day].dropna()):
            if fill_hours == hours:
                week.loc[index, day] = f'{employee_name} {hours}'
                break
        if hours == FULL_TIME[:-1]:
            for idx, val in enumerate(week[day].dropna()):
                if val == FIRST_HALF[:-1]:
                    week.drop(axis=day, index=idx, inplace=True)
                    week.reset_index(inplace=True, drop=True)
                    break
            for idx, val in enumerate(week[day].dropna()):
                if val == SECOND_HALF[:-1]:
                    week.drop(axis=day, index=idx, inplace=True)
                    week.reset_index(inplace=True, drop=True)
                    break
        if hours == FIRST_HALF[:-1]:
            for idx, val in enumerate(week[day].dropna()):
                if val == FULL_TIME[:-1]:
                    week.drop(axis=day, index=idx, inplace=True)
                    week.reset_index(inplace=True, drop=True)
                    break
        if hours == SECOND_HALF[:-1]:
            for idx, val in enumerate(week[day].dropna()):
                if val == FULL_TIME[:-1]:
                    week.drop(axis=day, index=idx, inplace=True)
                    week.reset_index(inplace=True, drop=True)
                    break
        week.to_csv(f'Расписание на {WEEK}.csv', sep=';', encoding='utf-8')
        return True
    except Exception:
        return False


############################################################################################################


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """
    :param message: Message
    """
    global employees
    user_id = message.from_user.id
    if user_id == 3815482200:
        btns.reply_key_board.row(btns.btn_create_schedule)
        await message.answer(text=MESSAGES['start_1'].format(user_name='Ислам'), reply_markup=btns.reply_key_board)

    elif user_id in employees['tg_id'].values and employees['name'].loc[employees['tg_id'] == user_id].values[0] != '0':
        user_name = employees['name'].loc[employees['tg_id'] == user_id].values[0]
        await message.answer(text=MESSAGES['start_1'].format(user_name=user_name), reply_markup=btns.reply_key_board)

    elif user_id in employees['tg_id'].values and employees['name'].loc[employees['tg_id'] == user_id].values[0] == '0':
        await message.answer(text=MESSAGES['start_3'])
        states.set_state(user_id=user_id, value=config.States.ENTER_NAME)

    else:
        await message.answer(text=MESSAGES['start_2'])
        employees = pd.concat([employees, pd.DataFrame([[user_id, '0', '0']], columns=employees.columns)],
                              ignore_index=True)
        employees.to_csv('employees.csv', sep=';', encoding='utf-8')
        states.set_state(user_id=user_id, value=config.States.ENTER_NAME)


@dp.message_handler(commands=['help'])
async def info(message: types.Message):
    """
    :param message:
    """
    text = MESSAGES['help']
    await message.reply(text)


@dp.message_handler(commands=['slots'])
async def show_slots(message: types.Message):
    """
    :param message: Message
    """
    await message.answer(MESSAGES['choose_day'], reply_markup=btns.days_key_board)


@dp.message_handler(commands=['Создать_расписание'])
async def creating_schedule_1(message: types.Message):
    """
    :param message: Message
    """
    await message.reply(MESSAGES['create_schedule'])


@dp.message_handler(commands=['schedule'])
async def send_schedule(message: types.Message):
    """
    :param message: Message
    """
    global WEEK
    try:
        with open(f'Расписание на {WEEK}.csv', 'rb') as f:
            await message.reply_document(f)
    except Exception:
        await message.reply(text=MESSAGES['schedule_error'])


@dp.message_handler(lambda message: states.get_current_state(message.from_user.id)[0] == config.States.ENTER_NAME)
async def entering_name(message: types.Message):
    """
    :param message:
    """
    name = message.text
    tg_id = message.from_user.id
    try:
        employees.loc[employees['tg_id'] == tg_id, 'name'] = name
        employees.to_csv('employees.csv', sep=';', encoding='utf-8')
        states.set_state(message.from_user.id, config.States.ON_WORK)
        await message.reply(text=MESSAGES['meeting_success'])
    except Exception:
        await message.reply(text=MESSAGES['meeting_error'])


@dp.callback_query_handler(lambda c: c.data in callback_words.keys() or c.data in FILL_HOURS.keys())
async def callback_worker(call: types.CallbackQuery):
    """
    :param call: CallbackQuery
    """
    mess = call.data
    if mess in list(callback_words.keys())[:-1]:
        day = mess
        day_mess = callback_words[day]
        hours = check_day(day)
        key_board = hours_buttons(hours)
        await bot.send_message(call.from_user.id, text=MESSAGES['slots'].format(day=day_mess), reply_markup=key_board)
    if mess == list(callback_words.keys())[-1]:
        await bot.send_message(call.from_user.id, text=MESSAGES['back'], reply_markup=btns.days_key_board)
    if mess in FILL_HOURS.keys():
        day_mess = call.message.text.split()[0]
        day = DAYS[day_mess]
        user_id = call.from_user.id
        hours = FILL_HOURS[mess]
        ok = fill_slot(day=day, user_id=user_id, hours=hours)
        if ok:
            await bot.send_message(call.from_user.id, text=MESSAGES['slot_selected'].format(day=day_mess, hours=hours))
            await bot.send_message(call.from_user.id, text=MESSAGES['choose_day'], reply_markup=btns.days_key_board)
        elif not ok:
            await bot.send_message(call.from_user.id,
                                   text=MESSAGES['slot_selection_error'].format(day=day_mess, hours=hours))
            await bot.send_message(call.from_user.id, text=MESSAGES['choose_day'], reply_markup=btns.days_key_board)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    await bot.delete_message(call.from_user.id, call.message.message_id)


@dp.message_handler()
async def creating_schedule_2(message: types.Message):
    """
    This function creates schedule right in the bot, by on of the users.
    By default, it's the user with user_id == 3815482200 (that's me, this bot createre)
    :param message: Message
    """
    global WEEK
    message_first_word = message.text.split()[0].capitalize()
    if message_first_word == 'Неделя':
        WEEK = message.text.split()[1]
        create_schedule(WEEK)
        await message.reply(MESSAGES['fill_schedule_day'])
    if message_first_word in DAYS.keys():
        try:
            bl = int(message.text.split()[1])
            al = int(message.text.split()[2])
            fill_schedule(bl=bl, al=al, day=message_first_word, week=WEEK)
            await message.reply(text=MESSAGES['success_day_fill'].format(day=message_first_word))
        except Exception:
            await message.reply(MESSAGES['error'])


if __name__ == '__main__':
    executor.start_polling(dp)
