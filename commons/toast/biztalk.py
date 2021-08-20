# -*- coding: utf-8 -*-
import re
import requests
import json


class ToastBizTalk:
    def __init__(self, appkey, secret_key, friend_id):
        self.TOAST_BIZMESSAGE_APPKEY = appkey
        self.TOAST_BIZMESSAGE_SECRETKEY = secret_key
        self.FRIEND_ID = friend_id

    def send_toast_mtalk(self, templateCode, recipientData):
        """ function send_mtalk
        :return:
        """
        url = 'https://api-alimtalk.cloud.toast.com/alimtalk/v1.4/appkeys/{appkey}/messages'.format(appkey=self.TOAST_BIZMESSAGE_APPKEY)
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "X-Secret-Key": self.TOAST_BIZMESSAGE_SECRETKEY
        }
        payload = {
            "plusFriendId": self.FRIEND_ID,
            'templateCode': templateCode,
            'recipientList': [recipientData]
        }

        try:
            r = requests.post(
                url,
                data=json.dumps(payload),
                headers=headers
            )
            data = r.json()
            res = data['header']['isSuccessful']
            sendResults = data['message']['sendResults']
            return res, sendResults
        except:
            return False, None