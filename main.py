import requests
from shapely.geometry.polygon import Polygon

from airport import ICAO
from boundry import inside

FIR = Polygon([(29.3, 123.5), (23.3, 124), (21, 121.2),
               (21, 117.3), (22.5, 117.3), (24.5, 120.2)])
AN = Polygon([(29.3, 123.5), (26.0, 121.5), (24.5, 121.3), (24.5, 123.7)])
AE = Polygon([(25.5, 121.5), (25.5, 123.5), (23.3, 123.6),
              (21, 121.3), (21, 117.6), (23.1, 120)])
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

    # seat = []
    # seat.append({'AN': f'{c_AN}'})
    # seat.append({'AW': f'{c_AW}'})
    # seat.append({'AE': f'{c_AE}'})
    # seat.append({'AS': f'{c_AS}'})
    # seat.append({'Error': f'{c_error}'})
    seat = {}
    seat['AN'] = f'{c_AN}'
    seat['AW'] = f'{c_AW}'
    seat['AE'] = f'{c_AE}'
    seat['AS'] = f'{c_AS}'

    sectors = ['AN', 'AW', 'AS', 'AE']
    html_col = ''
    for s in sectors:
        # print(s, seat[s])
        html_col += f"""
        <div class="col">
            <div class="card mb-3 rounded-3 shadow-sm">
                <div class="card-header py-4">
                <h1 class="display-1">{seat[s]}</h1>
                <h4>{s}</h4>
                </div>
            </div>
        </div> """

    return html_col


if __name__ == "__main__":
    r = run()
    print(r)
