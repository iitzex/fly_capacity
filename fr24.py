import requests
import json


def feed():
    headers = {
        'authority': 'data-live.flightradar24.com',
        'sec-ch-ua': '^\\^',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71',
        'accept': '*/*',
        'origin': 'https://www.flightradar24.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.flightradar24.com/',
        'accept-language': 'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-CN;q=0.5',
    }

    params = (
        ('bounds', '29.00,20.32,113.15,128.97'),
        ('faa', '0'),
        ('satellite', '1'),
        ('mlat', '0'),
        ('flarm', '0'),
        ('adsb', '1'),
        ('gnd', '0'),
        ('air', '1'),
        ('vehicles', '0'),
        ('estimated', '1'),
        ('maxage', '14400'),
        ('gliders', '0'),
        ('stats', '1'),
        ('enc', ''),
    )

    r = requests.get(
        'https://data-live.flightradar24.com/zones/fcgi/feed.js', headers=headers, params=params)

    try:
        j = r.json()
        print(j)

    except json.decoder.JSONDecodeError as e:
        print(e)
    return j
