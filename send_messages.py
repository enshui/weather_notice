#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
' weather_notice '
 
__author__ = 'Yu Enshui'

import json
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
import requests
from datetime import datetime

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

ACCESS_KEY_ID = "xxxxx"
ACCESS_KEY_SECRET = "xxxxx"
acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def send_sms(business_id, phone_numbers, template_param=None, sign_name='xxxx'):
    # 设定模板参数，决定使用哪个模板
    if datetime.today().hour < 12:
        # 发送今天的天气信息
        template_code='SMS_137658318'
    else:
        # 发送明天的天气信息
        template_code='SMS_137673296'
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    return smsResponse

def get_weather_content():
    response = requests.get('http://api.yuenshui.cn/weather/').text
    response = json.loads(response)
    result = response.get('result')
    keys = [k for k,v in result.items()][:2]
    if datetime.today().hour < 12:
        message = result.get(keys[0])
        message['date'] = keys[0]
    else:
        message = result.get(keys[1])
        message['date'] = keys[1]
    message['content']="%s，%s到%s度，%s风" % (message.get('weather'),message.get('low_temperature'),message.get('high_temperature'),message.get('wind_info'))
    return message


if __name__ == '__main__':
    phone_numbers = '185xxxx'
    __business_id = uuid.uuid1()
    m = get_weather_content()
    params = "{\"content\":\"%s\",\"date\":\"%s\"}" % (m.get('content'),m.get('date'))
    send = send_sms(__business_id, phone_numbers=phone_numbers,template_param=params)
    print(send)
