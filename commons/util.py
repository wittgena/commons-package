# -*- coding: utf-8 -*-

import xmltodict
import json


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
        return {}


def check_list_values_not_in_dict(l, map):
    necessary_items = [v for k, v in map.items() if v not in l]

    if necessary_items:
        return False, ', '.join(necessary_items)

    return True, ''


def get_list_values_from_dict(l, map):
	return dict(filter(lambda x: x[1] in l, map.items()))