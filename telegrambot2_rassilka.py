import telebot
import requests
import sqlite3
import schedule
import time
from telebot.apihelper import ApiTelegramException

conn = sqlite3.connect('db/db_weatherbot_tg.db', check_same_thread=False)
cursor = conn.cursor()


bot = telebot.TeleBot("TOKEN")
CHANNEL_NAME = "@Prognoz_pogodi_po_gorodam_bot"


def get_weather_volgograd(name):
    api_url = "http://api.openweathermap.org/data/2.5/weather"
    city = "Волгоград"
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
    return (f"""{name}, на данный момент в городе {city.title()}:
                температура {template} °C,
                по ощущениям {feeling} °C,
                скорость ветра {speed} м/с,
                облачность {clouds}%."""
            )

def weather_token_func_volgograd():
            try:
                city = "Волгоград"
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


def rassilka():
    lst = []
    for user_id1 in cursor.execute(f'SELECT user_id, user_name FROM test'):
        lst.append((user_id1[0], user_id1[1]))
    for i in lst:
        try:
            bot.send_message(i[0], get_weather_volgograd(i[1]))
            bot.send_sticker(i[0], weather_token_func_volgograd())
        except ApiTelegramException:
            people_id = i[0]
            cursor.execute(f'DELETE FROM test WHERE user_id = {people_id}')
            conn.commit()


def main():
    schedule.every().day.at('23:25:50').do(rassilka)
    schedule.every().day.at('06:30:00').do(rassilka)
    schedule.every().day.at('11:00:00').do(rassilka)
    schedule.every().day.at('14:30:00').do(rassilka)
    schedule.every().day.at('16:30:00').do(rassilka)

    while True:
        schedule.run_pending()



if __name__ == '__main__':
    main()






