from aiogram import Bot, Dispatcher, executor, types
import random
import sqlite3

bot = Bot('6679155946:AAHgWWKKfj-hFPuvFIZvm-g3-mCcHnH931c')
dp = Dispatcher(bot)

manicure = {'length': '', 'form': '', 'style': '', 'color': ''}
k=1

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup_start = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True,
                                             input_field_placeholder="Создай свой уникальный стиль")
    bt1 = types.KeyboardButton('💎Начать игру🎮')
    markup_start.add(bt1)
    await message.answer(
        f'Привет, {message.from_user.first_name}, этот бот поможет тебе определиться с дизайном маникюра',
        reply_markup=markup_start)

@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    markup_info = types.InlineKeyboardMarkup(resize_keyboard=True)
    bt1=types.InlineKeyboardButton('Связаться с админом💬', url='https://t.me/vldwrr')
    markup_info.add(bt1)
    await message.answer('Для того, чтобы задать свой вопрос, нажмите на кнопку', reply_markup=markup_info)


@dp.message_handler(content_types=['text'])
async def game(message: types.Message):

    global k

    if message.text == '💎Начать игру🎮' or message.text == '🎮Начать игру заново🔁':
        markup_first_round = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        bt1 = types.KeyboardButton('🎲Определить длину📐')
        markup_first_round.add(bt1)
        await bot.send_photo(message.chat.id, photo=open('images/length.jpg', 'rb'),
                             caption=f"Раунд 1️⃣ - выбор длины ногтей!\n\n🟨 <b>короткие</b>\n\n🟨 <b>средние</b>\n\n🟨 <b>длинные</b>",
                             reply_markup=markup_first_round, parse_mode='html')
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute(
            'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, user_id varchar(50), length varchar(50),'
            ' form varchar(50), style varchar(50), color_type varchar(50), color varchar(50))')
        conn.commit()
        cur.close()
        conn.close()
        k+=1

    elif message.text == '🎲Определить длину📐':
        manicure['length'] = ','.join(random.choices(['длинные', 'средние', 'короткие']))
        markup_second_round = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        bt1 = types.KeyboardButton('🎲Определить форму🔲')
        markup_second_round.add(bt1)
        await message.answer(f"<i>🎰Длина подобрана✅</i>", parse_mode='html')
        await bot.send_photo(message.chat.id, photo=open('images/form.jpg', 'rb'),
                             caption="Раунд 2️⃣ - выбор формы ногтей!\n\n<b>⬜️ овал\n\n⬜️ квадрат\n\n⬜️ миндаль\n\n⬜️ стилет</b>",
                             reply_markup=markup_second_round, parse_mode='html')

    elif message.text == '🎲Определить форму🔲':
        if manicure['length'] == 'короткие':
            manicure['form'] = ','.join(random.choices(['квадрат', 'овал']))
        else:
            manicure['form'] = ','.join(random.choices(['квадрат', 'овал', 'миндаль', 'стилет']))
        markup_third_round = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        bt1 = types.KeyboardButton('🎲Определить дизайн👩‍🎨')
        markup_third_round.add(bt1)
        await message.answer(f"<i>🎰Форма подобрана✅</i>", parse_mode='html')
        await bot.send_photo(message.chat.id, photo=open('images/style.jpg', 'rb'),
                             caption="Раунд 3️⃣ - выбор собственного дизайна ногтей!<b>\n\n🟪 стемпинг\n\n🟪 слайдеры\n\n🟪 линии\n\n🟪 френч\n\n🟪 блестки\n\n🟪 градиент</b>",
                             reply_markup=markup_third_round, parse_mode='html')
        rand=random.randint(2,8)
        if k% rand==0:
            await bot.send_photo(message.chat.id, photo=open('images/add.jpg', 'rb'))

    elif message.text == '🎲Определить дизайн👩‍🎨':
        manicure['style'] = ','.join(random.choices(['стемпинг', 'слайдеры', 'линии', 'френч', 'блестки', 'градиент']))
        markup_fourth_round = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        bt1 = types.KeyboardButton('🎲Определить цвет☀️')
        markup_fourth_round.add(bt1)
        await message.answer(f"<i>🎰Дизайн подобран✅</i>", parse_mode='html')
        await bot.send_photo(message.chat.id, photo=open('images/color.jpg', 'rb'),
                             caption="Раунд 4️⃣ - выбор цвета ногтей!<b>\n\n🟧 яркий\n\n🟧 нюд</b>",
                             reply_markup=markup_fourth_round, parse_mode='html')

    elif message.text == '🎲Определить цвет☀️':
        manicure['color'] = ','.join(random.choices(['яркий', 'нюд']))
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        bt1 = types.KeyboardButton('Показать дизайн')
        markup.add(bt1)
        await message.answer(f"<i>🎰Цвет подобран✅</i>", parse_mode='html', reply_markup=markup)
        if manicure['color'] == 'яркий':
            color = "(" + ",".join(random.choices(
                ["красный", "оранжевый", "желтый", "зеленый", "голубой", "синий", "фиолетовый", "розовый", "белый",
                 "черный", "серый", "коричневый", "бежевый", "малиновый", "грушевый", "оливковый", "лимонный",
                 "персиковый", "сиреневый", "мятный", "мандариновый", "карамельный", "аметистовый", "лазурный",
                 "аквамариновый", "бардовый", "золотистый", "серебряный", "индиго", "циан", "терракотовый",
                 "коралловый", "хаки", "вишневый", "орхидея"])) + ")"
        else:
            color = "(" + ",".join(random.choices(
                ["пастельно-розовый", "нежно-бежевый", "молочный", "мягкий карамельный", "небесно-голубой",
                 "нежно-зеленый", "светло-серый", "сиреневый", "кремовый"])) + ")"

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute(f"INSERT INTO users (user_id, length, form, style, color_type, color) "
        f"VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"
                   % (message.from_user.id, manicure['length'], manicure['form'], manicure['style'], manicure['color'], color))
        conn.commit()
        cur.close()
        conn.close()

    elif message.text == 'Показать дизайн':
            markup_restart = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True,
                                                       input_field_placeholder="Создай свой уникальный стиль")
            bt1 = types.KeyboardButton('🎮Начать игру заново🔁')
            markup_restart.add(bt1)
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()

            cur.execute('SELECT * from users WHERE user_id = ?', (message.from_user.id,))
            users = cur.fetchall()
            for elem in users:
                    await message.answer(
                    f"<b>⭐️Получившийся дизайн:🍀</b>\n\n▫️ длина - <b>{elem[2]}</b>\n▫️ форма - <b>{elem[3]}</b>\n▫️ дизайн - <b>{elem[4]}</b>\n▫️ цвет - <b>{elem[5]}{elem[6]}</b>",
                    reply_markup=markup_restart, parse_mode='html')
            cur.execute('DELETE from users WHERE user_id = ?', (message.from_user.id,))
            conn.commit()
            cur.close()
            conn.close()
executor.start_polling(dp)
