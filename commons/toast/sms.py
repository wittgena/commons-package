# -*- coding: utf-8 -*-
import re
import requests
import json


def check_receiver(receiver):
    receiver = receiver.replace('-','')
    if not re.findall(r'01\d{8,9}', receiver):
        return False, receiver
    else:
        return True, receiver


class ToastSMS:
    def __init__(self, appkey, sned_no):
        self.TOAST_SMS_APPKEY = appkey
        self.SEND_NO = send_no

    def send_toast_sms(self, receiver, message):
        """ function send_sms
        :return:
        """
        url = 'https://api-sms.cloud.toast.com/sms/v2.3/appKeys/{appKey}/sender/sms'.format(appKey=self.TOAST_SMS_APPKEY)
        headers = {
            "Content-Type": "application/json;charset=UTF-8"
        }
        payload = {
            'body': message,
            'sendNo': self.send_no,
            'recipientList': [
                {'recipientNo': receiver}
            ]
        }

        try:
            r = requests.post(
                url,
                data=json.dumps(payload),
                headers=headers
            )
            data = r.json()
            res = data['header']['isSuccessful']
            resultMessage = data['header']['resultMessage']
            return res, resultMessage
        except:
            return False, None

    def send_toast_mms(self, receiver, title, message):
        """ function send_toast_mms
        :return:
        """
        url = 'https://api-sms.cloud.toast.com/sms/v2.3/appKeys/{appKey}/sender/mms'.format(appKey=self.TOAST_SMS_APPKEY)
        headers = {
            "Content-Type": "application/json;charset=UTF-8"
        }
        payload = {
            'title': title,
            'body': message,
            'sendNo': self.SEND_NO,
            'recipientList': [
                {'recipientNo': receiver}
            ]
        }

        try:
            r = requests.post(
                url,
                data=json.dumps(payload),
                headers=headers
            )
            data = r.json()
            res = data['header']['isSuccessful']
            resultMessage = data['header']['resultMessage']
            return res, resultMessage
        except:
            return False, None
