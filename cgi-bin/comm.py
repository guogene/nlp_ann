#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import datetime
import os

from base_cgi import TASK_DATA_PATH


def load_local_json(filename):
    with open(filename, encoding="utf8") as f:
        data = f.read()
    try:
        data = json.loads(data)
    except:
        data = {}

    return data


def save_local_json(data, filename):
    try:
        data = json.dumps(data)
    except:
        return False
    with open(filename, "w", encoding="utf8") as f:
        f.write(data)

    return True


def query_task_data_file():
    files_list = []
    for root, dirs, files in os.walk(TASK_DATA_PATH):
        files_list += files
    files_list = [os.path.splitext(x)[0].encode("utf8", errors='surrogateescape').decode("utf8") for x in files_list]

    return files_list


def query_task_file_name(task):
    files_list = []
    for root, dirs, files in os.walk(TASK_DATA_PATH):
        files_list += files
    files_list = [os.path.splitext(x)[0].encode("utf8", errors='surrogateescape').decode("utf8") for x in files_list]
    for f in files_list:
        if f == task:
            return f
    return None


def get_today_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def get_now_date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%s")
