import json
import random
import time

import requests
import csv

headers = {
    'authority': 'www.nic.ru',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru,en;q=0.9',
    'content-type': 'application/json;charset=UTF-8',
    'cookie': 'pofm_cid=656732316e207; user_unic_ac_id=d6522254-a2f4-3490-9fcd-efa97d9340eb; _ga=GA1.2.1060957297.1701261875; _ym_uid=1701261875816719138; _ym_d=1701261875; WhiteInvader_closed_23739=true; session=ddddf560254915546118215b5c398ce98e93fecd6e1b750fea75f27e880f1e46; advcake_session=1; _gid=GA1.2.154388629.1701686428; _ga_cid=1060957297.1701261875; _ym_isad=2; WhiteCallback_visitorId=14681643622; WhiteCallback_visit=24089805892; WhiteSaas_uniqueLead=no; _ym_visorc=b; blitzlng=ru; _ga_YBVZ79X7XD=GS1.2.1701686428.3.1.1701686468.20.0.0; _ga_XTN6WH8J0D=GS1.2.1701686428.3.1.1701686468.20.0.0; WhiteCallback_openedPages=yuguv.UUizT; WhiteCallback_mainPage=UUizT; WhiteCallback_timeAll=142; WhiteCallback_timePage=142; session=ddddf560254915546118215b5c398ce98e93fecd6e1b750fea75f27e880f1e46',
    'origin': 'https://www.nic.ru',
    'referer': 'https://www.nic.ru/shop/category/?filters%5Bzones%5D=ru&sort=-newness',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.686 YaBrowser/23.9.5.686 Yowser/2.5 Safari/537.36',
    'x-client-fingerprint': 'f9095a596504b69364b152e3daf609a9'
}


def main():
    url = 'https://www.nic.ru/app/v1/get/domain-shop/lot/list'
    page = 1
    region = input('Введите регион')
    with open('result.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Домен', 'Цена', 'Валюта', 'Торг'])
        while True:
            payload = json.dumps({"pager": {"page": page, "perPage": 100}, "sort": "-newness",
                                  "filter": {"categories": [], "rubrics": [], "zones": [region]}, "lang": "ru"})
            response = requests.request("POST", url, headers=headers, data=payload).json()
            if response['body']['items'] != []:
                for item in response['body']['items']:
                    name = item['name']
                    price = str(item['prices'][0]['ask']).replace('.', ',')
                    currency = str(item['prices'][0]['currency'])
                    haggle = item['haggle']['isAbleTo']
                    if haggle:
                        haggle = 'Возможен торг'
                    else:
                        haggle = 'Без торга'
                    writer.writerow([name, price, currency, haggle])
                time.sleep(random.randint(1, 3))
                print(f"Записал {page * 100} доменов")
                page += 1
            else:
                print('Поиск окончен')
                break


if __name__ == '__main__':
    main()
