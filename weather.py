from datetime import datetime
import pymongo
import requests
from lxml import etree



def get_information():
    response = requests.get('http://forecast.weather.com.cn/town/weathern/101120504010.shtml')
    selector = etree.HTML(response.content)

    today_weather = selector.xpath('//li[@class="blue-item active"]')
    later_weather = selector.xpath('//li[@class="blue-item"]')
    weather_lists = today_weather + later_weather

    weather=[w.xpath('.//p[@class="weather-info"]/@title')[0] for w in weather_lists]
    wind_origin = [w.xpath('.//div[@class="wind-container"]/i[1]/@title')[0] for w in weather_lists]
    wind_final = [w.xpath('.//div[@class="wind-container"]/i[2]/@title')[0] for w in weather_lists]
    wind_info = [w.xpath('.//p[@class="wind-info"]/text()')[0].strip() for w in weather_lists]

    temperatures = selector.xpath('/html/body/div[4]/div[3]/div[1]/div/script/text()')[0].split()
    high_temperature = temperatures[8].replace(';', '').replace(']','').replace('[','').replace('"','').split(',')[1:6]
    low_temperature = temperatures[12].replace(';', '').replace(']','').replace('[','').replace('"','').split(',')[1:6]

    today_date = selector.xpath('//ul[@class="date-container"]//li[@class="date-item active"]//p[@class="date"]//text()')
    later_date = selector.xpath('//ul[@class="date-container"]//li[@class="date-item"]//p[@class="date"]//text()')[1:]
    date_lists=today_date + later_date

    result = dict()
    for i in range(5):
        data = dict()
        data['weather'] = weather[i]
        data['wind_origin'] = wind_origin[i]
        data['wind_final'] = wind_final[i]
        data['wind_info'] = wind_info[i]
        data['high_temperature'] = high_temperature[i]
        data['low_temperature'] = low_temperature[i]
        result[date_lists[i]] = data
    print(result)
    return result


def save_to_mongo():

    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.apis
    collection = db.weather

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data=dict()
    data['scrapy_date'] = now
    data['location']='小门家镇'
    data['result'] = get_information()
    collection.insert_one(data)

    client.close()


if __name__ == '__main__':
    save_to_mongo()
