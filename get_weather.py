

import requests


def read_weather():
    key = '70b9a3b1868610ff859131851ee630d2'
    lat = '10.045162'
    lon = '105.746857'

    # https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={API key}
    
    url = 'https://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lon + '&appid=' + key
    response = requests.get(url)
    data = response.json()
    temp = data['main']['temp'] - 273.15
    humi = data['main']['humidity']
    return temp, humi

print(read_weather())