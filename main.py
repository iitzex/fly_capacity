import time

import pandas as pd
import requests
from shapely.geometry.polygon import Polygon

from airport import ICAO
from boundry import inside

FIR = Polygon([(29.3, 123.5), (23.3, 124.5), (21, 121.2),
               (21, 117.3), (22.5, 117.3), (24.5, 120.2)])
AN = Polygon([(29.3, 123.5), (25.5, 121.5), (24.5, 122), (25.5, 123.5)])
AE = Polygon([(25.5, 121.5), (25.5, 123.5), (23.3, 123.6),
              (21, 121.3), (21, 118.6), (23.1, 120)])
AS = Polygon([(23.1, 120), (21, 117.3), (23.4, 117.3), (24.7, 118.5)])
AW = Polygon([(23.1, 120), (24.7, 118.5), (25.5, 120.5), (25.1, 121.3)])


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

    return r.json()


def flights():
    j = feed()
    # print(j)

    count = 0
    table = []
    for k, v in j.items():
        if k == 'full_count' or k == 'version' or k == 'stats' or \
                k == 'visible' or k == 'selected-aircraft' or k == 'copyright':
            continue

        level = int(v[4])
        if level < 18000:
            continue

        callsign = v[16]
        if callsign == '':
            continue

        lat = float(v[1])
        lon = float(v[2])

        if not inside(FIR, lat, lon):
            continue
        if inside(AN, lat, lon):
            sector = 'AN'
        elif inside(AE, lat, lon):
            sector = 'AE'
        elif inside(AS, lat, lon):
            sector = 'AS'
        elif inside(AW, lat, lon):
            sector = 'AW'
        else:
            sector = "None"

        src = ICAO(v[11])
        dst = ICAO(v[12])

        count = count + 1
        row = {
            'cs': callsign,
            'lat': lat,
            'lon': lon,
            'alt': level,
            'from': src,
            'to': dst,
            'sector': sector
            # 'timestamp': int(time.time())
        }
        # print(count, callsign, lat, lon, level, src, dst)
        table.append(row)

    # df = pd.DataFrame(table)
    # df = df.set_index('cs')
    return table


if __name__ == "__main__":
    table = flights()

    for v in table:
        print(v)
