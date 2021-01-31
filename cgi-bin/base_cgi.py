#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import cgi, cgitb
import json
import os
import sys
import urllib.parse


TASK_DATA_PATH = "/home/ann_data/task_data"
LABEL_DATA_PATH = "/home/ann_data/label_data.json"
LABEL_TEMPLETE_PATH = "/home/ann_data/label_templete.json"
USER_INFO_PATH = "/home/ann_data/user_info.json"

from auth import Auth


class BaseCgi:

    request_user = None

    def __init__(self, debug=False, auth=False):
        self.debug = debug
        if self.debug:
            print("Content-type:text/html")
            print("")

        if auth:
            self.auth_verify()

    def request_headers(self):
        cgi.print_environ()
        # cgi.parse_header()

    def get_request_token(self):
        token = os.environ.get("HTTP_TOKEN")
        return token

    def get_request_uri(self):
        return os.environ["REQUEST_URI"]

    def get_reuqest_method(self):
        return os.environ['REQUEST_METHOD']

    def is_json_request(self):
        content_type = os.environ["CONTENT_TYPE"]
        if content_type == "application/json":
            return True
        return False

    def load_query_params(self):
        uri = self.get_request_uri()
        res = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(uri).query))
        return res

    def load_form_data(self):
        if self.is_json_request() or self.get_reuqest_method() == "GET":
            return {}
        form = cgi.FieldStorage()
        return form

    def load_json_request(self):
        try:
            con = int(os.environ["CONTENT_LENGTH"])
            req_body = sys.stdin.read(con)
            req_body = req_body.encode("utf8", errors='surrogateescape').decode("utf8")
            my_dict = json.loads(req_body)
        except:
            my_dict = {}
        return my_dict

    def auth_verify(self):
        token = self.get_request_token()
        if not token:
            self.respone_json(status=-500, msg="无权限访问")
        try:
            username, token = token.split("_")
        except:
            self.respone_json(status=-500, msg="token异常")
        ret = Auth(username, token).verify_token()
        if not ret:
            self.respone_json(status=-500, msg="无效token")

        self.request_user = username

    def respone_json(self, data=None, status=200, msg="success"):
        print("Content-type:application/json")
        print("")
        res = {
            "status": status,
            "msg": msg,
            "data": data
        }
        print(json.dumps(res))
        sys.exit(0)
