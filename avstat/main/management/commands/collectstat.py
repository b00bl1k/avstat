import cfscrape
import re
from random import randint
from time import sleep

import datetime
from django.core.management.base import BaseCommand

from main.models import User, Stat

URL = "http://avto-nomer.ru/aktivuserall?galak=0&start={}"
TOP_PAGES = 15


def parse_stat(page):
    matches = re.findall(r"""
        <tr>
            <td>
                <span>\d+</span>
            </td>
            <td>
                <span><a\s+href=\'/user(\d+)\'>(.*?)</a></span>
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
            "name": match[1],
            "total": int(match[2].replace(" ", "")),
            "added": added
            })

    return retval


class Command(BaseCommand):
    help = 'Collect statistics'

    def handle(self, *args, **options):
        scraper = cfscrape.create_scraper()
        date = datetime.datetime.now() + datetime.timedelta(days=-1)

        for page in range(TOP_PAGES):
            self.stdout.write(f"Page {page}")
            response = scraper.get(URL.format(page)).text
            stat = parse_stat(response)
            for item in stat:
                user, created = User.objects.get_or_create(
                    id=item['id'],
                    defaults={'id': item['id'], 'name': item['name']}
                )
                if created:
                    self.stdout.write(f"User {item['name']}: ", ending="")
                    self.stdout.write(self.style.SUCCESS('CREATED'))

                stat, created = Stat.objects.get_or_create(
                    user=user, created_at=date,
                    defaults={
                        'user': user, 'created_at': date,
                        'total': item['total'], 'added': item['added'],
                    }
                )
                if not created:
                    self.stdout.write(f"Stat {date} for user {item['name']}: ", ending="")
                    self.stdout.write(self.style.WARNING('EXIST'))

            sleep(randint(2, 10))
