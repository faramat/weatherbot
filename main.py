import requests
import datetime #библиотека для отображения времени рассвета и заката
from config import open_weather_token #импортируем токен
from pprint import pprint #библиотека для вида json
def get_weather(city,open_weather_token): #функция принимающая 2 параметра,город и токен 

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
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric" 
            #обращение по апи
        )
        data = r.json()
        #pprint(data)
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
        print(f"----{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}----\n")
        print(f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Давление: {pressure}\n"
              f"Влажность: {humidity}%\nСкорость ветра: {wind}м/с\n"
              f"Страна: {country}\nРассвет: {sunrise_timestamp}\nЗакат: {sunset_timestamp}\n"
              f"Продолжительность дня: {lenght_of_the_day}\n"
             )
    except Exception as ex:
        print(ex)
        print("Проверьте название города")

def main():
    city = input("Введите город: ") #запрос у пользователя
    get_weather(city, open_weather_token) #вызов функции

if __name__ == '__main__':
    main()