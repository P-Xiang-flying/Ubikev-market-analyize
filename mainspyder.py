
import time
from datetime import datetime
import logging
import json
import csv
import requests
class mainspyder(object):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s : %(message)s', filename='log.txt')
    url = ['https://apis.youbike.com.tw/api/front/station/all?lang=tw&type=1','https://apis.youbike.com.tw/api/front/station/all?lang=tw&type=2']
    
    headers={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'apis.youbike.com.tw',
        'Origin': 'https://kcg.youbike.com.tw',
        'Referer': 'https://kcg.youbike.com.tw/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
        }
    def download_loaction(self):
        with open('location.csv', 'w', newline='',encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'status',
                'station_no',
                'name',
                'district',
                'address',
                'parking_spaces',
                'lat',
                'lng'
                ])
            for i in self.url:
                response = requests.get(i,headers=self.headers)
                dataJson = json.loads(response.text)
                dataJson =dataJson['retVal']
                for eachlocation in dataJson:
                    writer.writerow([
                        eachlocation['status'],
                        eachlocation['station_no'],
                        eachlocation['name_tw'],
                        eachlocation['district_tw'],
                        eachlocation['address_tw'],
                        eachlocation['parking_spaces'],
                        eachlocation['lat'],
                        eachlocation['lng']
                        ])
        print('location download done')
    def init_data(self):
        with open('time_list.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'time_id',
                'time'
                ])
        with open('station_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'time_id',
                'station_no',
                'avalible_spaces',
                'empty_spaces',
                'forbidden_spaces'
                ])
        print('init done')
    def spyder_data(self,count):
        timeNow=datetime.now()
        for i in self.url:
            response = requests.get(i,headers=self.headers)
            dataJson = json.loads(response.text)
            dataJson =dataJson['retVal']
            with open('time_list.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    count,
                    timeNow
                    ])
            with open('station_data.csv', 'a', newline='') as csvfile:
                 writer = csv.writer(csvfile)
                 for each_data in dataJson:
                    writer.writerow([
                    count,
                    each_data['station_no'],
                    each_data['available_spaces'],
                    each_data['empty_spaces'],
                    each_data['forbidden_spaces']
                    ])
        print(str(count)+' done')
        # Line通知
    def lineNotifyMessage(self, msg):
       headers = {
           "Authorization": "Bearer KtkgNfZqn06sMTAsmy5xZ9ExeHMPtswW9yPK43y5ARx",
           "Content-Type" : "application/x-www-form-urlencoded"
       }

       payload = {'message': msg}
       r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
       return r.status_code


mainspyder().download_loaction()
 mainspyder().init_data()
 count=0
 while 1:
     count +=1
     try:
         mainspyder().spyder_data(count)
     except Exception as e:
         print('error:'+str(count))
         logging.error('error'+str(count),exc_info=True)
         mainspyder().lineNotifyMessage('time_ID:'+str(count)+'\n'+str(datetime.now())+'\n'+str(e.args[0]))
     time.sleep(300)