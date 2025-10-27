from my_token import token
import telebot
import random
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot(token)

with open('.venv/bin/tilt_vopros.json', 'r', encoding='utf-8') as f:
    tilt_vopros = json.load(f)
with open('.venv/bin/turnir.json', 'r', encoding='utf-8') as f:
    tournaments = json.load(f)
with open('.venv/bin/mlbb_hero.json', 'r', encoding='utf-8') as f:
        mlbb_heroes = json.load(f)
with open('.venv/bin/test.json', 'r', encoding='utf-8') as f:
        questions_hero = json.load(f)
prophecies = [
    "Сегодня твой кор залетит во все патчи ⚡",
    "Лейла снова делает игру, но только если ты не фидишь 🔫",
    "Судьба благоволит твоему мейну — бей с ноги, только не промахнись 💥",
    "Твоя команда удивит тебя... возможно, даже приятным образом 😏",
    "Если пикнешь танка — спасёшь всех 💧",
    "Не доверяй лесу сегодня, он сам себе на уме 🌲",
    "Сегодня не день стрелков — пикай новарию с пронзой 🔮",
    "У врагов лаги, пользуйся моментом 😎",
    "Играй с хуком Франко, а не с рангом 💫",
    "Предсказания не будет, удали игру",
    "ММР — лишь иллюзия, настоящая сила в глобал мурчалке ⚔️"
]

#это наши статы по тестам и тп
statka = {}
ritual_statka = {}
hero_test_statka = {}


@bot.message_handler(commands=['start'])
def hello(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    knopka1 = KeyboardButton('Предсказание')
    knopka2 = KeyboardButton('Кто ты из млбб?')
    knopka3 = KeyboardButton('Ближайшие турниры')
    knopka4 = KeyboardButton('Ритуал победы')
    knopka5 = KeyboardButton('Тест на тильт')

    markup.row(knopka1, knopka2)
    markup.row(knopka3)
    markup.row(knopka4, knopka5)

    bot.send_message(
        message.chat.id,
        'Привет, дорогой игрок!\n'
        'Это бот-помощник по игре MLBB.\n'
        'С чем тебе сегодня помочь?',
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def send_message(message):
    user_id = message.chat.id

    if message.text == 'Предсказание':
        predskazanie = random.choice(prophecies)
        bot.send_message(user_id, f'🔮 Твое предсказание на сегодня:\n\n{predskazanie}')


    #
    elif message.text == "Тест на тильт":
        if user_id not in statka:
            statka[user_id] = {'vopros': 0, 'da': 0}
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton('Да'), KeyboardButton('Нет'))
            bot.send_message(user_id, "🧠 Начинаем тест на тильт! Отвечай 'Да' или 'Нет'.")
            bot.send_message(user_id, tilt_vopros[0], reply_markup=markup)
        else:
            bot.send_message(user_id, "Ты уже проходишь тест — отвечай на вопросы!")

    elif user_id in statka:
        state = statka[user_id]
        otvet = message.text.lower().strip()

        if otvet not in ['да', 'нет']:
            bot.send_message(user_id, 'Ты что, тупой? Ответь "да" или "нет".')
            return

        if otvet == 'да':
            state['da'] += 1
        state['vopros'] += 1

        # если есть ещё вопросы
        if state["vopros"] < len(tilt_vopros):
            bot.send_message(user_id, tilt_vopros[state["vopros"]])
        else:
            score = state["da"]
            del statka[user_id]
            if score <= 2:
                resul_tata = "🧘 Ты святой..."
            elif 3 <= score <= 5:
                resul_tata = "😬 Лёгкий тильт — ещё держишься, но скоро встанешь афк."
            elif 6 <= score <= 8:
                resul_tata = "🔥 Классический тильт — все бездари, кроме тебя."
            else:
                resul_tata = "💀 Всё плохо. Пора сделать перерыв."

            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row(KeyboardButton('Предсказание'), KeyboardButton('Кто ты из млбб?'))
            markup.row(KeyboardButton('Ближайшие турниры'))
            markup.row(KeyboardButton('Ритуал победы'), KeyboardButton('Тест на тильт'))
            bot.send_message(
                user_id,
                f"Результат теста: {score} из {len(tilt_vopros)} 'да'.\n\n{resul_tata}",
                reply_markup=markup
            )


    elif message.text == 'Ритуал победы':
        ritual_statka[user_id] = 0
        bot.send_message(user_id, "🕯️ Ритуал победы начат! Нажми 'Далее' для первого шага.")
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("Далее"))
        bot.send_message(user_id, "Шаг 1: Сделай глубокий вдох и расслабься.", reply_markup=markup)
    elif user_id in ritual_statka:
        step = ritual_statka[user_id]
        if message.text == "Далее":
            step += 1
            ritual_statka[user_id] = step
            if step == 1:
                bot.send_message(user_id, "Шаг 2: Визуализируй свою победу и командную координацию.")
            elif step == 2:
                bot.send_message(user_id, "Шаг 3: Скажи 'стоп, мне неприятно'.")
            elif step == 3:
                bot.send_message(user_id, "🔥Ритуал завершён! Идём побеждать!")

                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                knopka1 = KeyboardButton('Предсказание')
                knopka2 = KeyboardButton('Кто ты из млбб?')
                knopka3 = KeyboardButton('Ближайшие турниры')
                knopka4 = KeyboardButton('Ритуал победы')
                knopka5 = KeyboardButton('Тест на тильт')
                markup.row(knopka1, knopka2)
                markup.row(knopka3)
                markup.row(knopka4, knopka5)

                bot.send_message(user_id, "Главное меню снова с тобой", reply_markup=markup)
                del ritual_statka[user_id]

    elif message.text == 'Кто ты из млбб?':
        hero_test_statka[user_id] = {"vopr": 0, "otv": []}
        question = questions_hero[0]["question"]
        options = questions_hero[0]["options"]
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for opt in options:
            markup.add(KeyboardButton(opt))
        bot.send_message(user_id, question, reply_markup=markup)
    elif user_id in hero_test_statka:
        state = hero_test_statka[user_id]
        otv = message.text
        state["otv"].append(otv)
        state["vopr"] += 1
        if state["vopr"] < len(questions_hero):
            question = questions_hero[state["vopr"]]["question"]
            options = questions_hero[state["vopr"]]["options"]
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            for opt in options:
                markup.add(KeyboardButton(opt))
            bot.send_message(user_id, question, reply_markup=markup)
        else:
            chosen_personaz = "Aggressive" if "Агрессивно" in state["otv"] or "Нет" in state["otv"] else "Strategic"
            nash_heroes = [h for h in mlbb_heroes if h["category"] == chosen_personaz]
            hero = random.choice(nash_heroes)
            bot.send_message(user_id, f"🦸‍♂️ Твой герой MLBB сегодня: {hero['name']} ({hero['role']})")
            del hero_test_statka[user_id]

            # Возвращаем старую  клаву
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row(KeyboardButton('Предсказание'), KeyboardButton('Кто ты из млбб?'))
            markup.row(KeyboardButton('Ближайшие турниры'))
            markup.row(KeyboardButton('Ритуал победы'), KeyboardButton('Тест на тильт'))
            bot.send_message(user_id, "Вы вернулись в главное меню.", reply_markup=markup)

    elif message.text == 'Ближайшие турниры':
        if tournaments:
            turik = "🏆 Ближайшие турниры:\n\n"
            for t in tournaments:
                turik += f"{t['name']} — {t['date']}\n"
            bot.send_message(user_id, turik)
        else:
            bot.send_message(user_id, "Турниры пока не найдены. Учись играть,бездарь")
    else:
        bot.send_message(user_id, "Выбери кнопку на клавиатуре ⬇️")

bot.polling()
