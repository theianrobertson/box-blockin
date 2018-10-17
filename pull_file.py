import os
import datetime
import time
import glob
import logging

import requests

URL = "http://opendata.toronto.ca/transportation/tmc/rescucameraimages/CameraImages/loc{}.jpg"
LOCATIONS = ["9304", "9303", "9302", "8004"]
FILES = 'files'

def image_exists(image_bytes, location):
    """Does an image exist already?  i.e. does it match the last for that location.

    Parameters
    ----------
    image_bytes : bytes
        The actual raw bytes
    location : str
        The string location code for the camera

    Returns
    -------
    bool
        True if the last picture matches
    """
    all_files = sorted(glob.glob(os.path.join(FILES, location + '_*.jpg')))
    if all_files:
        with open(all_files[-1], 'rb') as f:
            if f.read() == image_bytes:
                return True
    return False

def grab_location(location):
    """Download a location's current image if it doesn't already exist"""
    filename = location + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.jpg'
    path = os.path.join(FILES, filename)
    r = requests.get(URL.format(location), stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        image_bytes = r.raw.read()
        if not image_exists(image_bytes, location):
            with open(path, 'wb') as f:
                f.write(image_bytes)
            logging.info('Saved file {}'.format(filename))
        else:
            logging.info('Already there yo')

    else:
        logging.info('Could not get {}'.format(filename))

def grab_data():
    """Loop over all locations and download"""
    for location in LOCATIONS:
        grab_location(location)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    while True:
        grab_data()
        time.sleep(2 * 60)
