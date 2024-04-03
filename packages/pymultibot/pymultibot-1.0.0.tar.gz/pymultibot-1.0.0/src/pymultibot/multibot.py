"""
@author: Fawwaz Thoerif (AkasakaID)
@telegram: t.me/AkasakaID
@email: akasakaid.gov@gmail.com
"""

import time
import requests


class Multibot:
    def __init__(self, key: str):
        """
        key: multibot api key
        """
        self.key = key
        self.url_in = "http://api.multibot.in/in.php"
        self.url_res = "http://api.multibot.in/res.php"

    def logs(self, value: str):
        now = time.localtime()
        day = str(now.tm_mday).zfill(2)
        mon = str(now.tm_mon).zfill(2)
        year = str(now.tm_year).zfill(2)
        hour = str(now.tm_hour).zfill(2)
        minute = str(now.tm_min).zfill(2)
        sec = str(now.tm_sec).zfill(2)
        open("logs.txt", "a+").write(
            f"[{year}-{mon}-{day} {hour}:{minute}:{sec}] {value}\n"
        )

    def get_balance(self):
        params = {
            "key": self.key,
            "action": "userinfo",
        }
        while True:
            try:
                res = requests.get(self.url_res, params=params, timeout=30)
                if res.text.find("balance") >= 0:
                    return True, res.json()["balance"]

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout,
            ):
                print("[x] connection error / timeout ", flush=True, end="\r")
                time.sleep(1)
                print("                                  ", flush=True, end="\r")
                continue

    def get_result(self, task_id):
        params = {
            "key": self.key,
            "id": task_id,
        }
        while True:
            try:
                res = requests.get(self.url_res, params=params, timeout=30)
                self.logs(res.text)
                if res.text.find("CAPCHA_NOT_READY") >= 0:
                    print("[|] captcha is not ready ! ", flush=True, end="\r")
                    time.sleep(0.375)
                    print("[/] captcha is not ready ! ", flush=True, end="\r")
                    time.sleep(0.375)
                    print("[-] captcha is not ready ! ", flush=True, end="\r")
                    time.sleep(0.375)
                    print("[\\] captcha is not ready ! ", flush=True, end="\r")
                    time.sleep(0.375)
                    print("[|] captcha is not ready ! ", flush=True, end="\r")
                    time.sleep(0.375)
                    print("[/] captcha is not ready ! ", flush=True, end="\r")
                    time.sleep(0.375)
                    print("[-] captcha is not ready ! ", flush=True, end="\r")
                    time.sleep(0.375)
                    print("[\\] captcha is not ready ! ", flush=True, end="\r")
                    time.sleep(0.375)
                    print("                              ", flush=True, end="\r")
                    continue

                if res.text.find("ERROR_NOT_CAPTCHA_ID") >= 0:
                    return False, "ERROR_NOT_CAPTCHA_ID"

                if res.text.find("ERROR_CAPTCHA_UNSOLVABLE") >= 0:
                    return False, "ERROR_CAPTCHA_UNSOLVABLE"

                if res.text.find("WRONG_RESULT") >= 0:
                    return False, "WRONG_RESULT"

                if res.text.find("OK") >= 0:
                    break

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout,
            ):
                print("[x] connection error / timeout ", flush=True, end="\r")
                time.sleep(1)
                print("                                  ", flush=True, end="\r")
                continue

        status, token = res.text.split("|")
        if status != "OK":
            return False, status

        return True, token

    def hcaptcha_token(self, site_key: str, site_url: str):
        """
        site_key: hcaptcha sitekey (ex: a5f74b19-9e45-40e0-b45d-47ff91b7a6c2)
        site_url: web page that have hcaptcha_token
        """
        while True:
            params = {
                "key": self.key,
                "method": "hcaptcha",
                "sitekey": site_key,
                "pageurl": site_url,
            }
            res = requests.get(self.url_in, params=params)
            self.logs(res.text)
            if res.text.find("|") < 0:
                return False, res.text

            status, task_id = res.text.split("|")
            if status != "OK":
                return False, res.text

            res = self.get_result(task_id=task_id)
            return res

    def recaptchav2(self, site_key: str, site_url: str):
        """
        site_key: recaptcha v2 sitekey (ex: 6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-)
        site_url: web page that have recpatcha v2
        """
        while True:
            try:
                params = {
                    "key": self.key,
                    "method": "userrecaptcha",
                    "googlekey": site_key,
                    "pageurl": site_url,
                }
                res = requests.get(self.url_in, params=params)
                self.logs(res.text)
                if res.text.find("|") < 0:
                    return False, res.text

                status, task_id = res.text.split("|")
                if status != "OK":
                    return False, res.text

                res = self.get_result(task_id=task_id)
                return res

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout,
            ):
                print("[x] connection error / timeout ", flush=True, end="\r")
                time.sleep(1)
                print("                                  ", flush=True, end="\r")

    def image_ocr(self, image: str):
        """
        image: image with base64 encode
        """
        while True:
            try:
                data = {
                    "key": self.key,
                    "method": "universal",
                    "body": image,
                }
                res = requests.post(self.url_in, data=data)
                self.logs(res.text)
                if res.text.find("|") < 0:
                    return False, res.text

                status, task_id = res.text.split("|")
                if status != "OK":
                    return False, res.text

                res = self.get_result(task_id=task_id)
                return res

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout,
            ):
                print("[x] connection error / timeout ", flush=True, end="\r")
                time.sleep(1)
                print("                                  ", flush=True, end="\r")

    def anti_bot(self, data: dict):
        """
        example data :
        {
                "main": "the main image of question captcha with base64 format",
                // rel for the key and value is image of rel with base64 format,
                "1": "rel_1_base64",
                "2": "rel_2_base64",
                "3": "rel_3_base64",
        }

        """
        data["method"] = "antibot"
        data["key"] = self.key
        while True:
            try:
                res = requests.post(self.url_in, data=data, timeout=30)
                self.logs(res.text)
                if res.text.find("|") < 0:
                    return False, res.text

                status, task_id = res.text.split("|")
                if status != "OK":
                    return False, res.text

                res = self.get_result(task_id=task_id)
                return res

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout,
            ):
                print("[x] connection error / timeout ", flush=True, end="\r")
                time.sleep(1)
                print("                                  ", flush=True, end="\r")

    def upside_down(self, image_base64: str):
        """
        image_base64: captcha image in base64 format
        """
        data = {
            "key": self.key,
            "method": "upside",
            "body": image_base64,
        }
        while True:
            try:
                res = requests.post(self.url_in, data=data, timeout=30)
                self.logs(res.text)
                if res.text.find("|") < 0:
                    return False, res.text

                status, task_id = res.text.split("|")
                if status != "OK":
                    return False, res.text

                res = self.get_result(task_id=task_id)
                return res
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout,
            ):
                print("[x] connection error / timeout ", flush=True, end="\r")
                time.sleep(1)
                print("                                  ", flush=True, end="\r")

    def rscaptcha(self, image: str):
        """
        image: captcha image in base64 format
        """
        data = {
            "key": self.key,
            "method": "rscaptcha",
            "body": image,
        }
        while True:
            try:
                res = requests.post(self.url_in, data=data, timeout=30)
                self.logs(res.text)
                if res.text.find("|") < 0:
                    return False, res.text

                status, task_id = res.text.split("|")
                if status != "OK":
                    return False, res.text

                res = self.get_result(task_id=task_id)
                return res

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout,
            ):
                print("[x] connection error / timeout ", flush=True, end="\r")
                time.sleep(1)
                print("                                  ", flush=True, end="\r")
