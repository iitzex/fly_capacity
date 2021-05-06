import time

import pandas as pd
from shapely.geometry.polygon import Polygon

from airport import ICAO
from boundry import inside
from fr24 import feed

FIR = Polygon([28.6, 124),(23.4, 119), (22.6, 117.3), (20.6, 117.3), (21, 121.3), (23.3, 124)])
AN = Polygon([(25.2, 120.55), (24.37, 121.33), (24.46, 124), (28.6, 124), (27.24, 122.23)])
AW = Polygon([(25.2, 120.55), (25, 121.25), (24.37, 121.37), (24.2, 121.1), (23.2, 120.3), (23.1, 120), (23.4, 119.2)])
AS = Polygon([(23.5, 119), (23.1, 119.6), (22.13, 118.2), (21, 118.12), (21, 117.3), (23.6, 117.3)])
AE = Polygon([(24.39, 121.34), (24.46, 124),(23.30, 124), (21, 121.3),(21, 118.3),(22.14, 118.21),(23.06, 120.06), (23.00, 120.33)])

Volume = {'AN': 20, 'AW': 12, 'AS': 15, 'AE': 15}


def flights():
    j = feed()

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
            'sector': sector,
            'timestamp': int(time.time())
        }
        # print(count, callsign, lat, lon, level, src, dst)
        table.append(row)

    df = pd.DataFrame(table)
    print(df)
    return table


def run():
    c_AN = 0
    c_AE = 0
    c_AS = 0
    c_AW = 0
    c_error = 0
    table = flights()

    for v in table:
        # print(v)
        if v['sector'] == 'AN':
            c_AN = c_AN + 1
        elif v['sector'] == 'AE':
            c_AE = c_AE + 1
        elif v['sector'] == 'AS':
            c_AS = c_AS + 1
        elif v['sector'] == 'AW':
            c_AW = c_AW + 1
        else:
            c_error = c_error + 1

    seat = {}
    seat['AN'] = c_AN
    seat['AW'] = c_AW
    seat['AS'] = c_AS
    seat['AE'] = c_AE

    sectors = ['AN', 'AW', 'AS', 'AE']
    html_col = ''
    for s in sectors:
        # print(s, seat[s])
        danger_tag = ''
        if seat[s] >= Volume[s]:
            danger_tag = 'text-white bg-danger border-danger'

        html_col += f"""
        <div class="col">
            <div class="card mb-3 rounded-3 shadow-sm {danger_tag}">
                <div class="card-header py-4">
                <h1 class="display-1">{seat[s]}</h1>
                <h4>{s}</h4>
                </div>
            </div>
        </div> """
        # print(Volume[s])

    return html_col


if __name__ == "__main__":
    r = run()
    print(r)
