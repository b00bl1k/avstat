#!/bin/env python2
# -*- coding: utf-8 -*-

URL = "http://avto-nomer.ru/aktivuserall?galak=0&start={}"

import os
import re
import time
import sqlite3
import datetime
import cfscrape
import logging
from random import randint
from time import sleep

TOP_PAGES=15
FORMAT = "%(asctime)s:%(levelname)s:%(module)s:%(message)s"
cwd = os.path.dirname(os.path.abspath(__file__))
logfile_path = os.path.join(cwd, "avstat.log")
logging.basicConfig(filename=logfile_path, level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger('avstat')

def get_date():
    date = datetime.datetime.now() + datetime.timedelta(days=-1)
    date_str = datetime.datetime.strftime(date, "%Y-%m-%d")
    return date_str

def parse_stat(page):
    matches = re.findall(r"""
        <tr>
            <td>
                <span>\d+</span>
            </td>
            <td>
                <span><a\s+href=\'/user(\d+)\'>(\S+)</a></span>
            </td>
            <td>
                <span>
                    <a\s+href=\'/gallery\.php\?usr=\d+\'>
                        ([0-9\s]+)
                    </a>
                </span>\s+(.*?)
            </td>
        </tr>
        """, page, re.X)

    retval = []
    for match in matches:
        badge = match[3]
        added = 0
        if badge:
            result = re.search(r""">\+(\d+)<""", badge)
            if result:
                added = int(result.groups()[0])
        retval.append({
            "id": int(match[0]),
            "name": match[1].decode("utf-8"),
            "total": int(match[2].replace(" ", "")),
            "added": added
            })

    return retval

def migrate(db):
    schema_path = os.path.join(cwd, 'schema.sql')
    logger.debug("apply migration %s" % schema_path)
    with open(schema_path) as f:
        db.executescript(f.read().decode('utf8'))

def add_record(db, id, name, total, added, date):
    result = db.execute('SELECT id FROM users WHERE id = ?', (id, )).fetchone()
    if result is None:
        db.execute('INSERT INTO users(id, name) VALUES(?,?)', (id, name))

    db.execute('INSERT INTO stat(user_id, created, total, added) VALUES(?,?,?,?)',
        (id, date, total, added))

def main():
    start_time = time.time()
    db_path = os.path.join(cwd, 'stat.db')
    logger.debug("avstat started")
    logger.debug("use data base %s" % db_path)

    db = sqlite3.connect(db_path)
    scraper = cfscrape.create_scraper()
    date = get_date()
    logger.debug("previous date %s" % date)

    # migrate(db)

    for page in xrange(TOP_PAGES):
        response = scraper.get(URL.format(page)).content
        stat = parse_stat(response)
        for item in stat:
            add_record(db, item['id'], item['name'], item['total'], item['added'], date)
        db.commit()
        sleep(randint(2, 10))

    db.close()

    logger.debug("completed in %f seconds" % (time.time() - start_time))

if __name__ == '__main__':
    main()
