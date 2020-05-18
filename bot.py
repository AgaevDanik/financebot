import os

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,)
from telegram.ext import (
    CallbackContext,
    Updater,
    Filters,
    MessageHandler,)
from base import (
    take_statistic,
    clear_about_user,
    for_balance,
    take_text,
    logic_update,
    logic_insert,
    insert_in_account,
    update_in_account_plus,
    update_in_account_minus,
    insert_in_users,
    sellect_from_users,
)


def button_start_handler(chat_id, main_markup, update: Update, context: CallbackContext):
    user_name = update.message.chat.first_name
    print(user_name)
    if sellect_from_users(chat_id):
        update.message.reply_text(
            text='why did you wrote this?',
            reply_markup=main_markup,
        )
        logic_update(chat_id, '/start')
    else:
        update.message.reply_text(
            text=f'Привет, меня зовут GodFinance. Я помогу тебе вести учет '
                 'собственных рассходов. Пользование проходит при помощи '
                 'нажатия кнопок снизу. Удачи! Для обращения к разработчику'
                 ' отправляйте сообщения с содержанием символа "&" Пример: "Обращение &".'
                 ' Он прочитает по возможности.',
            reply_markup=main_markup,
        )
        insert_in_users(chat_id, user_name)
        insert_in_account(chat_id)
        logic_insert(chat_id, '/start')


def button_transport_handler(chat_id, text, update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Введите потраченую сумму',
        reply_markup=ReplyKeyboardRemove(),
    )
    logic_update(chat_id, '/start(-) МинусТранспорт')


def button_food_handler(chat_id, text, update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Введите потраченую сумму',
        reply_markup=ReplyKeyboardRemove(),
    )
    logic_update(chat_id, '/start(-) МинусПродукты')


def button_dress_handler(chat_id, text, update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Введите потраченую сумму',
        reply_markup=ReplyKeyboardRemove(),
    )
    logic_update(chat_id, '/start(-) МинусОдежда')


def button_goods_handler(chat_id, text, update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Введите потраченую сумму',
        reply_markup=ReplyKeyboardRemove(),
    )
    logic_update(chat_id, '/start(-) МинусПредметы')


def button_payments_handler(chat_id, text, update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Введите потраченую сумму',
        reply_markup=ReplyKeyboardRemove(),
    )
    logic_update(chat_id, '/start(-) МинусПлатежи')


def button_other_handler(chat_id, text, update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Введите потраченую сумму',
        reply_markup=ReplyKeyboardRemove(),
    )
    logic_update(chat_id, '/start(-) МинусПрочее')


def button_balance_handler(chat_id, text, update: Update, context: CallbackContext,):
    balance = for_balance(chat_id)
    text = f'Статистика показана за все время\nВаш баланс💵:{balance["Баланс"]}\nВы потратили ❌: {balance["Потрачено"]}\n' \
           f'Вы Заработали🤑: {balance["Заработано"]}'
    update.message.reply_text(
        text=text,
    )


def button_add_handler(chat_id, text, update: Update, context: CallbackContext,):
    add_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Транспорт'),
                KeyboardButton(text='Продукты')
            ],
            [
                KeyboardButton(text='Одежда'),
                KeyboardButton(text='Предметы')
            ],
            [
                KeyboardButton(text='Предметы'),
                KeyboardButton(text='Платежи')
            ],
            [
                KeyboardButton(text='Прочее'),
                KeyboardButton(text='Главное меню')
            ],
        ],
        resize_keyboard=True,
    )
    update.message.reply_text(
        text='Выбери категорию',
        reply_markup=add_markup,
    )
    logic_update(chat_id, '/start(-) Минус')


def button_not_add_handler(chat_id, text, update: Update, context: CallbackContext):
    plus_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Работа'),
                KeyboardButton(text='Дело/Бизнесс')
            ],
            [
                KeyboardButton(text='Пожертвования'),
                KeyboardButton(text='Другое')
            ],
            [
                KeyboardButton(text='Главное меню')
            ],

        ],
        resize_keyboard=True,
    )
    update.message.reply_text(
        text='Выбери источник дохода',
        reply_markup=plus_markup,
    )
    logic_update(chat_id, '/start(+) Плюс')


def button_statistic_minus_handler(main_markup, chat_id, text, update: Update, context: CallbackContext):
    state = take_statistic(chat_id, '-')
    update.message.reply_text(
        text=f'Вы потратили за все время\n'
             f'Транспорт: {state["Транспорт"]}\n'
             f'Продукты: {state["Продукты"]}\n'
             f'Одежда: {state["Одежда"]}\n'
             f'Предметы: {state["Предметы"]}\n'
             f'Платежи: {state["Платежи"]}\n'
             f'Прочее: {state["Прочее"]}\n ',
        reply_markup=main_markup,
    )
    logic_update(chat_id, '/start')


def button_statistic_plus_handler(main_markup, chat_id, text, update: Update, context: CallbackContext):
    state = take_statistic(chat_id, '+')
    update.message.reply_text(
        text=f'Ваш доход за все время\n'
             f'Работа: {state["Работа"]}\n'
             f'Дело/Бизнесс: {state["Дело/Бизнесс"]}\n'
             f'Пожертвования: {state["Пожертвования"]}\n'
             f'Другое: {state["Другое"]}\n',
        reply_markup=main_markup,
    )
    logic_update(chat_id, '/start')


def button_clear_handler(main_markup, chat_id, text, update: Update, context: CallbackContext):
    clear_about_user(chat_id)
    logic_update(chat_id, '/start')
    update.message.reply_text(
        text='Ваш баланс обнулен',
        reply_markup=main_markup,
    )


def button_help_handler(chat_id, text, update: Update, context: CallbackContext):
    user_name = update.message.chat.first_name + update.message.chat.last_name
    update.message.reply_text(
        text=f'Привет {user_name}, меня зовут GodFinance. Я помогу тебе вести учет '
             'собственных рассходов. Пользование проходит при помощи '
             'нажатия кнопок снизу. Удачи! Для обращения к разработчику'
             ' отправляйте сообщения с содержанием символа "&" Пример: "Обращение &".'
             ' Он прочитает по возможности.',
    )


def button_action_handler(chat_id, text, update: Update, context: CallbackContext):
    action_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Статистика расходов'),
                KeyboardButton(text='Статистика доходов')
            ],
            [
                KeyboardButton(text='Обнулить счёт'),
                KeyboardButton(text='Главное меню')
            ],
        ]
    )
    update.message.reply_text(
        text='Выберите действие',
        reply_markup=action_markup
    )
    logic_update(chat_id, '/start Действия')


def button_some_else(chat_id, text, update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Введите сумму дохода',
        reply_markup=ReplyKeyboardRemove(),
    )
    logic_update(chat_id, '/start(+) ПлюсДругое')


def button_work(chat_id, text, update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Введите сумму дохода',
        reply_markup=ReplyKeyboardRemove(),
    )
    logic_update(chat_id, '/start(+) ПлюсРабота')


def button_present(chat_id, text, update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Введите сумму дохода',
        reply_markup=ReplyKeyboardRemove(),
    )
    logic_update(chat_id, '/start(+) ПлюсПожертвования')


def button_business(chat_id, text, update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Введите сумму дохода',
        reply_markup=ReplyKeyboardRemove(),
    )
    logic_update(chat_id, '/start(+) ПлюсДело/Бизнесс')


def button_menu_handler(main_markup, chat_id, update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Меню:',
        reply_markup=main_markup,
    )
    logic_update(chat_id, '/start')


def message_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    text = update.message.text
    main_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='(+) Плюс'),
                KeyboardButton(text='(-) Минус')
            ],
            [
                KeyboardButton(text='Баланс'),
                KeyboardButton(text='Действия'),
            ],
            [
                KeyboardButton(text='Помощь')
            ],
        ],
        resize_keyboard=True,
    )
    answers = {
        'Баланс': button_balance_handler,
        'Помощь': button_help_handler,
        '(-) Минус': button_add_handler,
        '(+) Плюс': button_not_add_handler,
        'Действия': button_action_handler,
    }
    answers_minus = {
        'Транспорт': button_transport_handler,
        'Продукты': button_food_handler,
        'Одежда': button_dress_handler,
        'Предметы': button_goods_handler,
        'Платежи': button_payments_handler,
        'Прочее': button_other_handler,
    }
    answers_plus = {
        'Работа': button_work,
        'Дело/Бизнесс': button_business,
        'Пожертвования': button_present,
        'Другое': button_some_else,
    }
    answers_action = {
        'Обнулить счёт': button_clear_handler,
        'Статистика расходов': button_statistic_minus_handler,
        'Статистика доходов': button_statistic_plus_handler,
    }
    text_for_answers_minus_sphere = [
        '/start(-) МинусОдежда',
        '/start(-) МинусПредметы',
        '/start(-) МинусПлатежи',
        '/start(-) МинусПрочее',
        '/start(-) МинусТранспорт',
        '/start(-) МинусПродукты'
    ]
    text_for_answer_plus_sphere = [
        '/start(+) ПлюсДругое',
        '/start(+) ПлюсДело/Бизнесс',
        '/start(+) ПлюсПожертвования',
        '/start(+) ПлюсРабота',
    ]
    if text == 'Главное меню':
        button_menu_handler(main_markup, chat_id, update=update, context=context)
    if text == '/start':
        button_start_handler(chat_id, main_markup, update=update, context=context)
    elif take_text(chat_id) == '/start':
        if answers.get(text, None):
            answers.get(text)(chat_id, text, update=update, context=context)
    elif take_text(chat_id) == '/start(-) Минус':
        if answers_minus.get(text, None):
            answers_minus.get(text)(chat_id, text, update=update, context=context)
    elif take_text(chat_id) == '/start(+) Плюс':
        if answers_plus.get(text, None):
            answers_plus.get(text)(chat_id, text, update=update, context=context)
    elif take_text(chat_id) == '/start Действия':
        if answers_action.get(text, None):
            answers_action.get(text)(main_markup, chat_id, text, update=update, context=context)
    elif take_text(chat_id) in text_for_answers_minus_sphere:
        sphere = take_text(chat_id)
        sphere = sphere.replace('/start(-) Минус', '')
        update_in_account_minus(chat_id, sphere, float(text))
        logic_update(chat_id, '/start')
        update.message.reply_text(
            text='✅✅✅',
            reply_markup=main_markup,
        )
    elif take_text(chat_id) in text_for_answer_plus_sphere:
        sphere = take_text(chat_id)
        sphere = sphere.replace('/start(+) Плюс', '')
        update_in_account_plus(chat_id, sphere, float(text))
        logic_update(chat_id, '/start')
        update.message.reply_text(
            text='✅✅✅',
            reply_markup=main_markup,
        )
    else:
        pass


def main():
    updater = Updater(
        token=os.environ.get('TOKEN'),
        use_context=True
    )

    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
