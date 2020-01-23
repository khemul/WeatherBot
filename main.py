from flask_sslify import SSLify
from config import API_KEY_W
from flask import request
from flask import Flask
import requests
import json
import os

TOKEN = os.environ.get('TOKEN')

BASE_URL = 'https://api.telegram.org/bot' + TOKEN

app = Flask(__name__)
sslify = SSLify(app) #https for flask


payload = {'appid': API_KEY_W} #API key for openweathermap.org
url_wether = 'https://api.openweathermap.org/data/2.5/weather?q='


# Get data weather by city name
def get_weather(url, city, payload):
	url += city
	r = requests.post(url, params=payload)
	a = r.json()
	temp_kelvin = a['main']['temp']
	temp_cels = temp_kelvin - 272.15
	return float('{:.3f}'.format(temp_cels))# переработать!!!


def send_message(chat_id, text='Hello'):
	url = BASE_URL + '/sendMessage'
	answer = {'chat_id': chat_id, 'text': text}
	rq = requests.post(url, json=answer )
	return rq.json()


@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		r = request.get_json()
		city = r['message']['text']
		chat_id = r['message']['chat']['id']
		send_message(chat_id, get_weather(url_wether, city, payload))

		return '<h1>Hello!</h1>' #???

	return '<h1>Hello!</h1>'


if __name__ == '__main__':
	app.run()
