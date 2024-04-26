from flask import Flask, render_template, request, redirect, url_for

from flask import jsonify, make_response

import random
import firebase_admin
from firebase_admin import db

import requests

# import thread
import threading
import time
import datetime
import numpy as np
from tensorflow.keras.models import load_model
import json

# import Adafruit_DHT
# import RPi.GPIO as GPIO
# import time

# from gpiozero import DistanceSensor
# ultrasonic = DistanceSensor(echo=17, trigger=4)

from gmail_send import send_email


# GPIO.setmode(GPIO.BCM)
# pin_dht_sensor = 25



sender_email = ""
sender_password = ""
receiver_email = ""
subject = ""
body = "cảnh báo"
smtp_server = "smtp.gmail.com"
smtp_port = 587

# read file main_config.json

with open('main_config.json', 'r') as f:
    data = json.load(f)
    sender_email = data.get('username')
    sender_password = data.get('password')
    receiver_email = data.get('receiver_email')
    subject = data.get('subject')
    smtp_server = data.get('smtp_server')
    smtp_port = data.get('smtp_port')


print('sender_email:', sender_email)
print('sender_password:', sender_password)
print('receiver_email:', receiver_email)
print('subject:', subject)
print('smtp_server:', smtp_server)
print('smtp_port:', smtp_port)




app = Flask(__name__)


model = load_model('trained_model.h5')


water_caution_level = 100

is_send_mail = False



@app.route("/")
def about_page():
    # check cookie
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    print('username:', username)
    print('password:', password)
    if username == 'admin' and password == 'admin':
        return render_template('dashboard.html')
    return render_template('login.html')


# sign_out
@app.route("/sign_out", methods=['POST'])
def sign_out():
    response = make_response(jsonify({'message': 'Sign out successful'}))
    response.set_cookie('username', '', expires=0)
    response.set_cookie('password', '', expires=0)
    return response


# set_caution
@app.route("/set_caution", methods=['POST'])
def set_caution():
    global water_caution_level
    if request.method == 'POST':
        data = request.json
        caution = data.get('water_level')
        print('caution:', caution)
        water_caution_level = int(caution)
        # save to 
        return jsonify({'message': 'Set caution successful'})
    else:
        return jsonify({'message': 'Method not allowed'})

# login_admin
@app.route("/login_admin", methods=['POST'])
def login_admin():
    if request.method == 'POST':
        data = request.json  # Lấy dữ liệu gửi từ frontend dưới dạng JSON
        username = data.get('username')
        password = data.get('password')

        print('username:', username)
        print('password:', password)
        if username == 'admin' and password == 'admin':
            # save cookie
            response = make_response(jsonify({'message': 'Login successful', 'username': username}))
            response.set_cookie('username', username)
            response.set_cookie('password', password)
            return response
        else:
            return jsonify({'message': 'Login failed'})
    else:
        return jsonify({'message': 'Method not allowed'})
    

def read_dht11():
    # humi, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin_dht_sensor)
    humi, temp  = 0, 0

    if humi is not None and temp is not None:
        return temp, humi
    else:
        return 0, 0

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
    return round(temp, 2), round(humi, 2)

def read_water_level():
    # read data from water level
    # water_level = random.randint(0, 100)
    sum = 0
    for i in range(10):
        # sum += ultrasonic.distance
        sum += random.randint(0, 100)
        time.sleep(0.1)
    water_level = (sum / 10)
    return water_level


databaseURL = 'https://sample-736cc.firebaseio.com/'

cred_obj = firebase_admin.credentials.Certificate('firebase-adminsdk.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL':databaseURL
})

def send_data_firebase():


    global is_send_mail

    mytime = time.time()

    current_date = datetime.datetime.fromtimestamp(mytime).strftime('%d-%m-%Y')
    current_hours = datetime.datetime.fromtimestamp(mytime).strftime('%H')
    current_minutes = datetime.datetime.fromtimestamp(mytime).strftime('%M')
    history_path = '/history/' + current_date + '/' + current_hours + '/' + current_minutes 

    ref = db.reference('/data')
    history = db.reference(history_path)

    temp, humi = read_dht11()
    weather_temp, weather_humi = read_weather()
    water_level = read_water_level()

    next_day_data = np.array([temp, humi, water_level, 1, 24]).reshape(1, 5)
    prediction_water_level_1  = model.predict(next_day_data)[0][0]
    next_day_data = np.array([temp, humi, water_level, 1, 48]).reshape(1, 5)
    prediction_water_level_2  = model.predict(next_day_data)[0][0]

    print("water_level = ", type(water_level), water_level)
    print("water_caution_level = ", type(water_caution_level), water_caution_level)

    if water_level > water_caution_level and not is_send_mail:
        body = 'Cảnh báo mực nước sông vượt ngưỡng cảnh báo'
        body += '\nNhiệt độ: ' + str(temp)
        body += '\nĐộ ẩm: ' + str(humi)
        body += '\nNhiệt độ thời tiết: ' + str(weather_temp)
        body += '\nĐộ ẩm thời tiết: ' + str(weather_humi)
        body += '\nMực nước hiện tại: ' + str(water_level)
        body += '\nDự đoán mực nước 24h sau: ' + str(round(float(prediction_water_level_1), 2))
        body += '\nDự đoán mực nước 48h sau: ' + str(round(float(prediction_water_level_2), 2))
        body += '\nNgưỡng cảnh báo: ' + str(water_caution_level)


        send_email(sender_email, sender_password, receiver_email, subject, body, smtp_server, smtp_port)
        is_send_mail = True
        print('send email')
    elif water_level < water_caution_level:
        is_send_mail = False
        print('reset send email', water_level, water_caution_level)
    else:
        print("mail was sent")

    data = {
        'temp': temp,
        'humi': humi,
        'weather_temp': weather_temp,
        'weather_humi': weather_humi,
        'water_level': water_level,
        'prediction_water_level_1': round(float(prediction_water_level_1), 2),
        'prediction_water_level_2': round(float(prediction_water_level_2),2),
        'caution_level': water_caution_level
    }

    ref.set(data)
    history.push(data)
    print('send data to firebase:', data)

def send_data_firebase_thread():
    while True:
        send_data_firebase()
        time.sleep(15)

if __name__ == "__main__":
    _thread = threading.Thread(target=send_data_firebase_thread, args=())
    _thread.daemon = True
    _thread.start()
    app.run(debug=True,  host="0.0.0.0", port=5100)