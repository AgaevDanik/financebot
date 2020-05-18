import sqlalchemy as sa
from sqlalchemy.ext import declarative as dec
import os

DB_USER = os.environ.get("DB_USER")
DB_PASSWD = os.environ.get("DB_PASSWD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
breakpoint()
base = dec.declarative_base()
metadata = sa.MetaData()
engine = sa.create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True
)


class Logic(base):
    __tablename__ = "Logic"
    chat_id = sa.Column("chat_id", sa.Integer, nullable=False, primary_key=True,)
    text = sa.Column("text", sa.VARCHAR(60), default='')


class Account(base):
    __tablename__ = "Account"

    chat_id = sa.Column("chat_id", sa.Integer, nullable=False, primary_key=True,)
    state = sa.Column("state", sa.Float(2), default=0)
    income = sa.Column("income", sa.Float(2), default=0)
    outcome = sa.Column("outcome", sa.Float(2), default=0)
    transport = sa.Column("transport", sa.Float(2), default=0)
    food = sa.Column("food", sa.Float(2), default=0)
    dress = sa.Column("dress", sa.Float(2), default=0)
    goods = sa.Column("goods", sa.Float(2), default=0)
    payments = sa.Column("payments", sa.Float(2), default=0)
    other = sa.Column("other", sa.Float(2), default=0)
    work = sa.Column("work", sa.Float(2), default=0)
    business = sa.Column("business", sa.Float(2), default=0)
    some_else = sa.Column("some_else", sa.Float(2), default=0)
    present = sa.Column("present", sa.Float(2), default=0)


class Users(base):
    __tablename__ = "Users"

    id = sa.Column("user_id", sa.Integer, primary_key=True,)
    chat_id = sa.Column("chat_id", sa.Integer, nullable=False)
    name = sa.Column("name", sa.VARCHAR(60))


metadata.create_all(engine)


def take_statistic(chat_id, sign):
    with engine.connect() as connection:
        query = sa.select([Account]).where(Account.chat_id == chat_id)
        result_of_selection = connection.execute(query)
        if sign == '+':
            for sphere in result_of_selection:
                result = {
                    'Работа': sphere.work,
                    'Дело/Бизнесс': sphere.business,
                    'Другое': sphere.some_else,
                    'Пожертвования': sphere.present,
                }
                return result
        elif sign == '-':
            for sphere in result_of_selection:
                result = {
                    'Транспорт': sphere.transport,
                    'Продукты': sphere.food,
                    'Одежда': sphere.dress,
                    'Предметы': sphere.goods,
                    'Платежи': sphere.payments,
                    'Прочее': sphere.other,
                }
                return result


def clear_about_user(chat_id):
    with engine.connect() as connection:
        clear_in_account = upd = sa.update(Account).where(
            Account.chat_id == chat_id
        ).values(state=0, outcome=0, income=0, transport=0, food=0, dress=0, goods=0, payments=0, other=0, work=0,
                 business=0, some_else=0, present=0)
        connection.execute(clear_in_account)


def take_text(chat_id):
    with engine.connect() as connection:
        query = sa.select([Logic]).where(Logic.chat_id == chat_id)
        query_res = connection.execute(query)
        for txt in query_res:
            return txt.text


def logic_update(chat_id, text):
    with engine.connect() as connection:
        upd = sa.update(Logic).where(Logic.chat_id == chat_id).values(text=text)
        connection.execute(upd)


def logic_insert(chat_id, text):
    with engine.connect() as connection:
        ins = sa.insert(Logic).values({Logic.chat_id: chat_id, Logic.text: text})
        connection.execute(ins)


def for_balance(chat_id):
    with engine.connect() as connection:
        query = sa.select([Account]).where(Account.chat_id == chat_id)
        result = connection.execute(query)
        for digit in result:
            for_bal = {
                'Баланс': digit.state,
                'Потрачено': digit.outcome,
                'Заработано': digit.income,
            }
        return for_bal


def update_in_account_minus(chat_id, sphere, value):
    with engine.connect() as connection:
        query = sa.select([Account]).where(Account.chat_id == chat_id)
        sphere_result = connection.execute(query)

        for digit in sphere_result:
            sphere_an = {
                'Транспорт': digit.transport,
                'Продукты': digit.food,
                'Одежда': digit.dress,
                'Предметы': digit.goods,
                'Платежи': digit.payments,
                'Прочее': digit.other,
            }
            outcome_value = digit.outcome
            state_value = digit.state
            sphere_value = sphere_an[sphere]
        sphere_value += value
        outcome_value += value
        state_value -= value
        convert_sphere = {
            'Транспорт': 'transport',
            'Продукты': 'food',
            'Одежда': 'dress',
            'Предметы': 'goods',
            'Платежи': 'payments',
            'Прочее': 'other',
        }
        sphere_for_update = {
            convert_sphere[sphere]: sphere_value,
        }

        upd = sa.update(Account).where(
            Account.chat_id == chat_id
        ).values(state=state_value, outcome=outcome_value, **sphere_for_update)
        connection.execute(upd)


def update_in_account_plus(chat_id, sphere, value):
    with engine.connect() as connection:
        query = sa.select([Account]).where(Account.chat_id == chat_id)
        sphere_result = connection.execute(query)

        for digit in sphere_result:
            sphere_an = {
                'Работа': digit.work,
                'Дело/Бизнесс': digit.business,
                'Другое': digit.some_else,
                'Пожертвования': digit.present,
            }
            income_value = digit.income
            state_value = digit.state
            sphere_value = sphere_an[sphere]
        sphere_value += value
        income_value += value
        state_value += value
        convert_sphere = {
            'Работа': 'work',
            'Дело/Бизнесс': 'business',
            'Другое': 'some_else',
            'Пожертвования': 'present',
        }
        sphere_for_update = {
            convert_sphere[sphere]: sphere_value,
        }

        upd = sa.update(Account).where(
            Account.chat_id == chat_id
        ).values(state=state_value, income=income_value, **sphere_for_update)
        connection.execute(upd)


def insert_in_users(chat_id, name):
    with engine.connect() as connection:
        ins = sa.insert(Users).values({Users.chat_id: chat_id, Users.name: name})
        connection.execute(ins)
        return None


def insert_in_account(chat_id):
    with engine.connect() as connection:
        ins = sa.insert(Account).values({Account.chat_id: chat_id})
        connection.execute(ins)
        return None


def sellect_from_users(chat_id):
    with engine.connect() as connection:
        query = sa.select([Users.chat_id])
        result = connection.execute(query)
        ides = []
        for user in result:
            ides.append(user.chat_id)
        if chat_id in ides:
            return True
        else:
            return False

base.metadata.create_all(engine)
