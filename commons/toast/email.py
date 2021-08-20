# -*- coding: utf-8 -*-
import requests
import json


class ToastEmail:
    def __init__(self, app_key):
        self.TOAST_EMAIL_APPKEY = app_key

    def send_toast_email(self, from_email, from_name, to_email, subject, body):
        url = 'https://api-mail.cloud.toast.com/email/v1.6/appKeys/{appKey}/sender/mail'.format(appKey=self.TOAST_EMAIL_APPKEY)
        headers = {
            "Content-Type": "application/json;charset=UTF-8"
        }
        payload = {
            'senderAddress': from_email,
            'senderName': from_name,
            'title': subject,
            'body': body,
            'receiverList': [{
                'receiveMailAddr': to_email,
                'receiveType': 'MRT0'
            }]
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
