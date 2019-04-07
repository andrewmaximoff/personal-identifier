import datetime

import requests
import telegram

URL = 'http://127.0.0.1:8000/api/visit/registration/'
FAMILY_ID = '568f62ad-dd8a-4bde-b290-d7fcf9aece03'


def check_visits(visit_list: dict, names: list):
    change = False
    for name in names:
        if name in visit_list.keys():
            timedelta = (datetime.datetime.now() - visit_list[name]).total_seconds()
            if timedelta > float(30):
                visit_list[name] = datetime.datetime.now()
                change = True
        else:
            visit_list[name] = datetime.datetime.now()
            change = True
    return change


def event_visit(path_to_file: str, names: list):
    for name in names:
        data = {
            'username': name,
            'family_id': FAMILY_ID,
        }
        requests.post(URL, files={'file': open(path_to_file, 'rb')}, data=data)