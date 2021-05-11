# -*- coding: utf-8 -*-

from .helper import get_workbook

import traceback
import os

__ALL__ = ['RawExcelReader']


class RawExcelReader:
    def __init__(self, filename):
        self.filename = filename

    def read(self, positions):
        if not self.filename:
            return {}

        try:
            wb = get_workbook(self.filename)
            sheet = wb.active
        except Exception:
            traceback.print_exc()
            return {}

        values = {}
        for k, v in positions.items():
            try:
                values[k] = sheet[v].value
            except Exception:
                values[k] = None

        wb.close()
        return values
