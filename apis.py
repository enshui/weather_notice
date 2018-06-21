import json

from flask import Flask
import pymongo
import random

__all__ = ['app']

app = Flask(__name__)

MONGO_URL = 'localhost'
MONGO_DB = 'apis'

@app.route('/')
def index():
    return '<h2>Welcome to My Apis</h2>'

@app.route('/weather/')
def get_weather():
    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    result = db.weather.find({}, {'_id': 0}).limit(1).sort([('scrapy_date', -1)])
    # dumps: dict ת jscon
    result = json.dumps(list(result)[0], ensure_ascii=False)
    client.close()
    return result


if __name__ == '__main__':
    app.run(port=5000)
