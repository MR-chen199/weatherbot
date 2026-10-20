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
        f'城市: {forecast['city']}\n'
        f'日期: {weather['data']}\n'
        f'夜间天气: {weather['nightweather']}\n'
        f'白天温度: {weather['daytemp']}风\n'

          )
    else:
        print(f'请求失败,原因{data}')

def sendmail(self):
    message = MIMEText(self,'html','utf-8')
    message['From'] = Header('天气播报员','utf-8')
    message['To'] = Header('您好','utf-8')
    message['Subject']=Header('每日天气推送','utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL('smtp.qq.com',465)
        smtpObj.login(mail_user,mail_password)
        smtpObj.sendmail(mail_user,[mail_user],message.as_string())
        print('发送成功')
    except Exception as e:
        print('发送失败')
    finally:
        smtpObj.quit()

if __name__ == '__main__':
    print('正在获取天气')
    weather_info=getweather()
    print(weather_info)
    if'失败' not in weather_info:
        print('正在发送邮件')
        sendmail(weather_info)
