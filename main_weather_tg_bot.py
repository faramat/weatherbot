from aiogram.bot.api import Methods
import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города для отображения погоды!")

@dp.message_handler()
async def get_weather(message: types.Message):
    #словарь состояния погоды + эмодзи
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B",
    }
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric" 
            #обращение по апи
        )
        data = r.json()
        #последующее обращение к серверу за информацией
        city = data["name"]
        cur_weather = data["main"]["temp"]
        weather_description = data["weather"][0]["main"]
        #пишем условия совпадения ключей для эмодзи
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно"
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        country = data["sys"]["country"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lenght_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        #Вывод текущей даты и информации
        await message.reply(f"----{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}----\n")
        await message.reply(f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Давление: {pressure}\n"
              f"Влажность: {humidity}%\nСкорость ветра: {wind}м/с\n"
              f"Старана: {country}\nРассвет: {sunrise_timestamp}\nЗакат: {sunset_timestamp}\n"
              f"Продолжительность дня: {lenght_of_the_day}\n"
             )
    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)