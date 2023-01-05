start_message_1 = 'Привет, {user_name}! Чего желаешь?'
start_message_2 = 'Кажется, мы с тобой не знакомы. Давай это исправим! Как тебя зовут?'
start_message_3 = 'Кажется, мы с тобой начинали знакомиться! Давай продолжим. Как тебя зовут?'
meeting_success = 'Вот и познакомились! Имя записал!'
meeting_error = 'Что-то не вышло. Попробуй заново.'
slots = '{day}\nВот свободные слоты. Нажми, чтобы занять!'
choose_day = 'Выбери день недели'
error = 'Что-то не получилось'
create_schedule = 'Пришли даты недели в формате: "Неделя 14.11-18.11"'
fill_schedule_day = 'А теперь пришли количество детей на каждый день недели отдельно, в формате: '\
                    '"Понедельник 10 15". '\
                    'Где 10 - количество детей до обеда, 15 - количество детей после обеда'
success_day_fill = '{day} заполнен(а)'
schedule_error = 'Не получилось. Кажется, расписания еще нет.'
back = 'Вернулись'
slot_selected = 'Вы заняли слот "{day} {hours}"!'
slot_selection_error = 'Не получилось занять слот "{day} {hours}"! Либо слот уже занят, ' \
                       'либо вы уже выбрали себе слот в этот день.'
help_text = 'Это бот для составления расписания\nЕсли бот записал твое имя, то можно начинать. Чтобы посмотреть ' \
            'свободные рабочие слоты, нужно нажать на кнопку "Свободные слоты", далее выбрать день недели. ' \
            'Затем появятся свободные слоты. Нажав на понравившийся слот, ты его сразу займешь!' \
            '\nКнопка "Прислать расписание" пришлет тебе расписание в формате .csv, но, только если ' \
            'расписание существует.'

MESSAGES = {
    'start_1': start_message_1,
    'start_2': start_message_2,
    'start_3': start_message_3,
    'help': help_text,
    'slots': slots,
    'choose_day': choose_day,
    'error': error,
    'fill_schedule_day': fill_schedule_day,
    'success_day_fill': success_day_fill,
    'back': back,
    'slot_selected': slot_selected,
    'slot_selection_error': slot_selection_error,
    'create_schedule': create_schedule,
    'schedule_error': schedule_error,
    'meeting_success': meeting_success,
    'meeting_error': meeting_error
}
