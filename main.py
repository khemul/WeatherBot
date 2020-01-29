from flask import Flask
from flask_sslify import SSLify
from flask import request
import requests
import json
from config import API_KEY_W
from config import TOKEN

degree_sign= u'\N{DEGREE SIGN}'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN

app = Flask(__name__)
sslify = SSLify(app)

#***************************************************************
payload = {'lang': 'ru', 'units': 'metric','appid': API_KEY_W}
url_wether = 'https://api.openweathermap.org/data/2.5/weather?q='


def get_weather(url, city, payload):
	url += city
	r = requests.post(url, params=payload)
	data = r.json()

	weather = data['weather'][0]['description']  # получаем данные о погоде (осадки, пасмурно, солнечно и тд. ...)
	pressure = data['main']['pressure'] * 0.75   # получаем значение атмосферного давления и переводим в мм. рт. ст.
	humidity = data['main']['humidity']          # получаем значение влажности
	temp = data['main']['temp']                  #получаем значение температуры

	result = '{3}.\nТемпература воздуха: {0:.1f}{4}\nДавление: {1:.0f} мм. рт.ст.\nВлажность: {2}%'.format(temp, pressure, humidity, weather, degree_sign)
	return result



def write_jason(data, filename='data.json'):
	with open(filename, 'w') as f:
		json.dump(data, f, indent=2, ensure_ascii=False)


def send_message(chat_id, text='Hello'):
	url = BASE_URL + 'sendMessage'
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

		return '<h1>POST</h1>'

	return '<h1>Hello!</h1>'


if __name__ == '__main__':
	app.run()
