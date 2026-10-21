from email.mime.multipart import MIMEMultipart

import requests
import os
from requests import session
import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os
import json
key = os.environ.get('AMAP_KEY')
city_adcode = '330100'
url = f'https://restapi.amap.com/v3/weather/weatherInfo?city={city_adcode}&key={key}&extensions=all'
mail_user='3353639017@qq.com'
mail_pass=os.environ.get('MAIL_PASS')
def getweather():
    response = requests.get(url)
    data = response.json()
    if data['status'] == '1':
       forecast = data['forecasts'][0]
       weather = forecast['casts'][1]
       msg=(
        f"城市: {forecast['city']}\n"
        f"日期: {weather['date']}\n"
        f"夜间天气: {weather['nightweather']}\n"
        f"白天温度: {weather['daytemp']}风\n"

          )
       return msg
    else:
        print(f'请求失败,原因{data}')

def sendmail(content):
    message = MIMEText(content,'html','utf-8')
    message['From'] = f'WeatherBot <{mail_user}>'
    message['To'] = f'Master <{mail_user}>'
    message['Subject']='每日天气推送'
    smtpObj = None
    try:
        smtpObj = smtplib.SMTP_SSL('smtp.qq.com',465)
        print('发送的邮箱为',mail_user)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(mail_user,[mail_user],message.as_string())
        print('发送成功')
    except Exception as e:
        print(f'发送失败,原因{e}')
    finally:
        if smtpObj is not None:
            try:
                smtpObj.quit()
            except:
                pass
if __name__ == '__main__':
    print('正在获取天气')
    weather_info=getweather()
    print(weather_info)
    if'失败' not in weather_info:
        print('正在发送邮件')
        sendmail(weather_info)


















