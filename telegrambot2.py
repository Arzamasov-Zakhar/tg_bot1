import telebot
import requests
import sqlite3
from telebot import apihelper
from telebot import types
import time


while True:
    try:

        conn = sqlite3.connect('db/db_weatherbot_tg.db', check_same_thread=False)
        cursor = conn.cursor()

        bot = telebot.TeleBot("TOKEN")
        CHANNEL_NAME = "@Prognoz_pogodi_po_gorodam_bot"


        def weather_token_func(city):
            try:
                api_url = "http://api.openweathermap.org/data/2.5/weather"
                params = {
                    "q": city,
                    "appid": "11c0d3dc6093f7442898ee49d2430d20",
                    "units": "metric"
                }
                res = requests.get(api_url, params=params)

                data = res.json()
                weather_token = data["weather"][0]["main"]
                weather_token_dict_day = {"Clouds": "CAACAgIAAxkBAAEOc51jRIGjONEVVNFfIR0V1_cS5kXKVAACYwMAAmOLRgxR7yWANo_4vCoE",
                                          "Snow": "CAACAgIAAxkBAAEOc3ljRICd2z_uqKS9Oer0LOiaKtLNTAACdAMAAmOLRgztBjKP1VO-GioE",
                                          "Rain": "CAACAgIAAxkBAAEOc3djRICPjj81IjN1FW1j1rpccQsWTAACZQMAAmOLRgwXTSc67Nm5BCoE",
                                          "Clear": "CAACAgIAAxkBAAEOc3NjRIBRPvCBR2MDUqEnt9hb5FboBgACaAMAAmOLRgx3R9fVwMzA9ioE",
                                          "Haze": "CAACAgIAAxkBAAEOc6djRIH0xBsT-YfJ9Fn8Qy0rtEXY-wACKgAD49Y-DwkpO-G6cMR4KgQ",
                                          "Mist": "CAACAgIAAxkBAAEOc6djRIH0xBsT-YfJ9Fn8Qy0rtEXY-wACKgAD49Y-DwkpO-G6cMR4KgQ",
                                          "Thunderstorm": "CAACAgIAAxkBAAEOc4tjRIEhoqb2asWS9mE4fCfmpRHC9gACZAMAAmOLRgzR1TmSZp5wqSoE", }

                weather_token_dict_night = {"Clouds": "CAACAgIAAxkBAAEOc61jRIKtynbiIrqcUN5Eo3Kc1vHtOAACawMAAmOLRgxWK64y5jZMUioE",
                                            "Snow": "CAACAgIAAxkBAAEOc69jRIK4ogMC3iBRcYifb7DeF4awDwACdgMAAmOLRgzULINCDFioASoE",
                                            "Rain": "CAACAgIAAxkBAAEOc7FjRILWktN76vH8a6nD5ipzrhjWuwACZQMAAmOLRgwXTSc67Nm5BCoE",
                                            "Clear": "CAACAgIAAxkBAAEOc6tjRIKZ_XW-m74Q3-hcpd1Tn2cnWAACZgMAAmOLRgxH_5x9Zs_eOCoE",
                                            "Haze": "CAACAgIAAxkBAAEOc6djRIH0xBsT-YfJ9Fn8Qy0rtEXY-wACKgAD49Y-DwkpO-G6cMR4KgQ",
                                            "Mist": "CAACAgIAAxkBAAEOc6djRIH0xBsT-YfJ9Fn8Qy0rtEXY-wACKgAD49Y-DwkpO-G6cMR4KgQ",
                                            "Thunderstorm": "CAACAgIAAxkBAAEOc4tjRIEhoqb2asWS9mE4fCfmpRHC9gACZAMAAmOLRgzR1TmSZp5wqSoE", }

                if time.time() < data["sys"]["sunrise"] or time.time() > data["sys"]["sunset"]:
                    # bot.send_sticker(m.from_user.id, weather_token_dict_night.get(weather_token))
                    return weather_token_dict_night.get(weather_token)
                else:
                    # bot.send_sticker(m.from_user.id, weather_token_dict_day.get(weather_token))
                    return weather_token_dict_day.get(weather_token)
            except KeyError:
                    return "CAACAgIAAxkBAAEOc8NjRIzHzmHk_gYF1mhP7ifcTukn-AACKwADj6PNDl18qbwekPa6KgQ"


        def get_weather(city: str):
            api_url = "http://api.openweathermap.org/data/2.5/weather"

            try:
                params = {
                    "q": city,
                    "appid": "11c0d3dc6093f7442898ee49d2430d20",
                    "units": "metric"
                }
                res = requests.get(api_url, params=params)

                data = res.json()
                template = round(data["main"]["temp"], 1)
                feeling = round(data["main"]["feels_like"], 1)
                speed = round(data["wind"]["speed"], 1)
                clouds = data["clouds"]["all"]
                return f"""На данный момент в городе {city.title()}:
                    температура {template} °C,
                    по ощущениям {feeling} °C,
                    скорость ветра {speed} м/с,
                    облачность {clouds}%."""

            except KeyError:
                return f"Введите, пожалуйста, корректное название города."


        @bot.message_handler(commands=["start"])
        def start(m, res=False):

            cursor.execute('''CREATE TABLE IF NOT EXISTS test (
                user_id INTEGER,
                user_name STRING,
                user_surname STRING,
                username STRING
              )''')
            us_id = m.from_user.id
            us_name = m.from_user.first_name
            us_sname = m.from_user.last_name
            username = m.from_user.username

            cursor.execute(f'SELECT user_id FROM test WHERE user_id = {us_id}')
            if cursor.fetchone() is None:
                cursor.execute(f'INSERT INTO test VALUES (?, ?, ?, ?)', (us_id, us_name, us_sname, username))
                conn.commit()
                bot.send_sticker(m.from_user.id,
                                 'CAACAgIAAxkBAAEObEtjQgH8oZrngIKCWSLh0ECRiqOtLAACOAADj6PNDgAB_YKn8TCetSoE')
            else:

                bot.send_sticker(m.from_user.id,
                                 'CAACAgIAAxkBAAEObE9jQgNeVKcK6CMLPcgMIyJZTvt4HwACNwADj6PNDpeRDA0i5vUlKgQ')

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            info = types.KeyboardButton("Информация")
            Volgograd = types.KeyboardButton("Волгоград")
            Rostov = types.KeyboardButton("Ростов-на-Дону")
            Moscow = types.KeyboardButton("Москва")
            markup.add(info, Volgograd, Rostov, Moscow)
            bot.send_message(m.chat.id, "Я на связи. "
                                        "Готов рассказать Вам о погоде. "
                                        "Чтобы узнать прогноз погоды в определенном городе, просто введите название города или выберите город из списка ниже.",
                             reply_markup=markup)


        @bot.message_handler(commands=['delete'])
        def delete(message):
            bot.send_sticker(message.from_user.id,
                             'CAACAgIAAxkBAAEObE1jQgMNGuyVDLs9yh4XDEP6TwywSgACLgADj6PNDm3KTY9gDxq7KgQ')

            people_id = message.from_user.id
            print(people_id)
            cursor.execute(f'SELECT user_id FROM test WHERE user_id = {people_id}')
            cursor.execute(f'DELETE FROM test WHERE user_id = {people_id}')
            conn.commit()


        @bot.message_handler(content_types=["text"])
        def handle_text(message):
            mat_list = ["хуй", "пизда", "гондо", "пидор", "педи", "педо", "педа", "чмо", "говн", "шлюх", "шлюц"]
            for i in mat_list:
                if i in message.text.lower():
                    return bot.send_message(message.chat.id, "ай, ай, ай, как не хорошо")

            if message.text == "Информация":
                bot.send_message(message.chat.id,
                                 "Чтобы узнать прогноз погоды в определенном городе, просто введите название города или выберите город из списка ниже.")
            else:
                bot.send_message(message.chat.id, get_weather(message.text))
                bot.send_sticker(message.chat.id, weather_token_func(message.text))


        bot.polling(none_stop=True, interval=0)

        apihelper.SESSION_TIME_TO_LIVE = 5 * 60

    except:
        pass
