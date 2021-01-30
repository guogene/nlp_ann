#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from base_cgi import USER_INFO_PATH
from comm import load_local_json, get_today_date
import hashlib


class Auth:
    SALT = "kdls223teststest"

    def __init__(self, username, token=None):
        self.user_info = load_local_json(USER_INFO_PATH)
        self.username = username
        self.token = token

    def verify_username(self):
        if not self.user_info:
            return False
        for item in self.user_info:
            if item["user_name"] == self.username:
                return item
        return False

    def verify_token(self):
        ret = self.verify_username()
        if not ret:
            return False
        today = get_today_date()
        origin_str = self.username + ret["password"] + self.SALT + today
        token = hashlib.md5(origin_str.encode(encoding='UTF-8')).hexdigest()
        if token != self.token:
            return False
        return True

    def gen_token(self, password):
        ret = self.verify_username()
        if not ret:
            return False
        if ret['password'] != password:
            return False
        today = get_today_date()
        origin_str = self.username + ret["password"] + self.SALT + today
        return hashlib.md5(origin_str.encode(encoding='UTF-8')).hexdigest()


if __name__ == '__main__':
    a = Auth("admin","849bdaad01591b74f130f662d0a6f573").verify_token()
    print(a)
