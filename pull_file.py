import os
import shutil
import datetime
import time

import requests

URL = "http://opendata.toronto.ca/transportation/tmc/rescucameraimages/CameraImages/loc{}.jpg"
LOCATIONS = ["9304", "9302"]
FILES = 'files'

def grab_location(location):
    filename = location + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.jpg'
    path = os.path.join(FILES, filename)
    r = requests.get(URL.format(location), stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        print('Saved file {}'.format(filename))
    else:
        print('Could not get {}'.format(filename))

def grab_data():
    for location in LOCATIONS:
        grab_location(location)

if __name__ == '__main__':
    while True:
        grab_data()
        time.sleep(3 * 60)
