import config
import pandas as pd


def get_current_state(user_id):
    """
    :param user_id: int
    :return: int
    """
    try:
        with open('employees.csv', encoding='utf-8') as emp:
            db = pd.read_csv(emp, delimiter=';', index_col=0)
            return db.loc[db['tg_id'] == user_id, 'state'].values
    except KeyError:
        return config.States.START


def set_state(user_id, value):
    """
    :param user_id: int
    :param value: int
    :return: bool
    """
    try:
        with open('employees.csv', encoding='utf-8') as emp:
            db = pd.read_csv(emp, delimiter=';', index_col=0)
            db.loc[db['tg_id'] == user_id, 'state'] = value
            db.to_csv('employees.csv', sep=';', encoding='utf-8')
            return True
    except Exception:
        return False
