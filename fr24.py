import requests
import json


def feed():
    headers = {
        'authority': 'data-live.flightradar24.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'origin': 'https://www.flightradar24.com',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        'dnt': '1',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'referer': 'https://www.flightradar24.com/24.39,121.06/6',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
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
    except json.decoder.JSONDecodeError as e:
        print(e)
    return j
