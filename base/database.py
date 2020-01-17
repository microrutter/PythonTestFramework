import logging
from datetime import datetime
import calendar
import psycopg2

import utilities.custom_logger as cl
from base.config import config
from base.date_time_manipultion import DateTimeMan


class DatabaseConnection:

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, section):
        self.params = config(section=section)
        self.dm = DateTimeMan()

    def connection(self):
        try:
            # connect to the PostgreSQL server
            self.log.info("Connecting to the PostgreSQL database...")
            return psycopg2.connect(**self.params)
        except (Exception, psycopg2.DatabaseError) as error:
            self.log.critical(error)

   