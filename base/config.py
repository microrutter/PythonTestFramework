import logging
from configparser import RawConfigParser

import utilities.custom_logger as cl


def config(filename="configfiles/database.ini", section="postgresql"):
    log = cl.customLogger(logging.DEBUG)
    # create a parser
    parser = RawConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
            log.info(param[1])
    else:
        log.critical("Section {0} not found in the {1} file".format(section, filename))

    return db
