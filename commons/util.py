# -*- coding: utf-8 -*-

import xmltodict
import json
from dateutil import parser, tz


def find_list_of_dict(list_of_dict, key, value):
    try:
        return next(
            (item for item in list_of_dict if item[key] == value),
            None
        )
    except Exception:
        return None


def get_chunks(lst, chunk_size):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def xmltojson(xml):
    try:
        res = xmltodict.parse(xml)
        res = json.dumps(res)
        res = json.loads(res)
        return res
    except Exception:
        logger.exception('')
        return {}


def check_map(row, map):
    necessary_items = []
    for k, v in map.items():
        if v not in row:
            necessary_items.append(v)

    if necessary_items:
        return False, ', '.join(necessary_items)
    return True, ''


def get_data_from_map(row, map):
    ret_data = {}
    for k, v in map.items():
        if v in row:
            ret_data[k] = row[v]
    return ret_data


def convert_datetime_timezone(time_str, source_timezone, target_timezone):
    source_zone = tz.gettz(source_timezone)
    target_zone = tz.gettz(target_timezone)
    org_time = parser.parse(time_str)
    org_time = org_time.replace(tzinfo=source_zone)
    return org_time.astimezone(target_zone)
