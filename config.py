callback_words = {'Monday': 'Понедельник', 'Tuesday': 'Вторник', 'Wednesday': 'Среда', 'Thursday': 'Четверг',
                  'Friday': 'Пятница', 'Back': 'Назад'}
FULL_TIME = '9:00 - 18:30,'
FIRST_HALF = '9:00 - 14:00,'
SECOND_HALF = '14:00 - 18:30,'
FIRST_MIDDLE = '10:00 - 16:00,'
SECOND_MIDDLE = '12:00 - 18:00,'
DAYS = {'Понедельник': 'Monday', 'Вторник': 'Tuesday', 'Среда': 'Wednesday', 'Четверг': 'Thursday', 'Пятница': 'Friday'}
HOURS = ['9:00 - 18:30', '9:00 - 14:00', '14:00 - 18:30', '10:00 - 16:00', '12:00 - 18:00']
FILL_HOURS = {'full': '9:00 - 18:30', 'first_half': '9:00 - 14:00',
              'second_half': '14:00 - 18:30', 'first_middle': '10:00 - 16:00',
              'second_middle': '12:00 - 18:00'}


class States:
    START = 0
    ENTER_NAME = 1
    ON_WORK = 2
