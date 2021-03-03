import csv
from os import listdir
from os.path import isfile, isdir

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

FIR = Polygon([(28.3, 124), (23.3, 124),
               (21, 121.2), (21, 117.3), (22.5, 117.3), (24.5, 120.2)])


def inside(sector, lat, lon):
    if sector.contains(Point(float(lat), float(lon))):
        return True
    else:
        return False


def check(fn):
    with open(fn, newline='') as f:
        track = csv.DictReader(f)
        status = 0
        msg = ''
        print('!', fn)
        for row in track:
            lat, lon = row['Position'].split(',')

            res = inside(lat, lon)
            if res == -status:
                msg += f"{status}, {lat}, {lon}, {row['UTC']}\n"

            status = res

        if msg != '':
            print(msg)


def traverse(path):
    dirs = listdir(path)
    for f in dirs:
        p = f'{path}/{f}'
        if isdir(p):
            traverse(p)
        if isfile(p) and 'csv' in p:
            check(p)


if __name__ == '__main__':
    r = inside(FIR, '25.843', '121.602')
    print(r)
