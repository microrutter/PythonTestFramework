import logging
import time
from datetime import datetime
from datetime import timedelta

import utilities.custom_logger as cl


class DateTimeMan:

    log = cl.customLogger(logging.DEBUG)

    def __init__(self):
        self.now = datetime.now()

    def minus_days_return_string(self, days=1):
        date = self.now - timedelta(days=days)
        return datetime.strftime(date, "%d/%m/%Y")

    def add_days_return_string(self, days=1):
        date = self.now + timedelta(days=days)
        return datetime.strftime(date, "%d/%m/%Y")

    def check_date(self, day):
        date = self.now + timedelta(days=1)
        if day < date:
            return True
        else:
            return False

    @staticmethod
    def string_date(date):
        if date:
            return datetime.strftime(date, "%Y-%m-%d")
        else:
            return None

    def check_date_now(self, day):
        return day > self.now.date()
