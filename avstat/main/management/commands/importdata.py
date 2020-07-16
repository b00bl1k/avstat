import sqlite3
from django.utils.timezone import get_current_timezone
from datetime import datetime
from django.core.management.base import BaseCommand
from main.models import User, Stat


class Command(BaseCommand):
    help = 'Import old database'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        db = sqlite3.connect(path)

        for row in db.execute('SELECT id, name FROM users'):
            self.stdout.write(f"Add {row[1]}: ", ending="")
            _, created = User.objects.get_or_create(
                id=row[0],
                defaults={'id': row[0], 'name': row[1]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS('OK'))
            else:
                self.stdout.write("EXIST")

        tz = get_current_timezone()
        for row in db.execute('SELECT id, user_id, created, total, added FROM stat'):
            user = User.objects.get(pk=row[1])
            date = tz.localize(datetime.strptime(row[2], '%Y-%m-%d'))
            self.stdout.write(f"Add {row[0]} {user.name} {date}: ", ending="")
            _, created = Stat.objects.get_or_create(
                user=user, created_at=date,
                defaults={
                    'user': user, 'created_at': date,
                    'total': row[3], 'added': row[4],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS('OK'))
            else:
                self.stdout.write("EXIST")
