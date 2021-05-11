# -*- coding: utf-8 -*-

import time
import logging
import requests

from slacker import Slacker
from FA.settings import SLACK_AIDKOREA_BACKOFFICE_TOKEN, DJANGO_ENV

logger = logging.getLogger('commons')

TEST_CHANNEL = '#backoffice-test'
DEBUG_CHANNEL = '#backoffice-logs'

NOTICES_CHANNEL = '#backoffice-notices' if DJANGO_ENV in ['test', 'prod'] else TEST_CHANNEL


def slack_notify_header(channel, header_msg):
    msg = """
----------------------------------
일시: %s
작업: %s
----------------------------------
    """
    request_time = time.strftime('%Y-%m-%d %H:%M:%s')
    slack_notify(channel, msg % (request_time, header_msg))


def slack_notify_error(channel, error_msg):
    msg = """
----------------------------------
에러: %s
일시: %s
----------------------------------
    """
    error_time = time.strftime('%Y-%m-%d %H:%M:%s')
    slack_notify(channel, msg % (error_time, error_msg))


def slack_debug(message):
    channel = DEBUG_CHANNEL if DJANGO_ENV in ['test', 'prod'] else TEST_CHANNEL

    if channel != DEBUG_CHANNEL:
        slack_notify(TEST_CHANNEL, message)


def slack_notify(channel, message):
    try:
        slack = Slacker(SLACK_AIDKOREA_BACKOFFICE_TOKEN)
        slack.chat.post_message(channel, message)
    except Exception:
        logger.exception('slack_notify exception')


def slack_notify_dm(emails, message):
    try:
        slack = Slacker(SLACK_AIDKOREA_BACKOFFICE_TOKEN)

        if DJANGO_ENV != 'prod':
            email = 'andy@aidkr.com'
            user = slack_get_user_from_email(email)
            slack.chat.post_message(user['id'], message)
        else:
            for email in emails:
                user = slack_get_user_from_email(email)
                slack.chat.post_message(user['id'], message)
    except Exception:
        logger.exception('slack_notify exception')


def slack_get_users():
    try:
        slack = Slacker(SLACK_AIDKOREA_BACKOFFICE_TOKEN)
        users = slack.users.list(True)
        logger.debug(users)
    except Exception:
        logger.exception('')


def slack_get_user_from_email(email):
    try:
        url = 'https://slack.com/api/users.lookupByEmail'
        headers = {'content-type': 'x-www-form-urlencoded'}
        data = {
            'token': SLACK_AIDKOREA_BACKOFFICE_TOKEN,
            'email': email
        }
        r = requests.get(url, data, headers=headers)
        data = r.json()
        logger.debug(data)
        return data['user']
    except Exception:
        return None
