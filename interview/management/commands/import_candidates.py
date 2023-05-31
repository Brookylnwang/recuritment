import csv

from django.core.management import BaseCommand
from interview.models import Candidate

# python manage.py import_candidates --path file.csv

class Command(BaseCommand):
    help = '从csv文件的内容读取候选人列表，导入数据库'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt', encoding='utf-8') as f:
            reader = csv.reader(f, dialect='excel')
            for row in reader:
                candidate = Candidate.objects.create(
                    username = row[0],
                    city = row[1],
                    phone = row[2],
                    bachelor_school = row[3],
                    major = row[4],
                    test_score_of_general_ability = row[6],
                    paper_score = row[7]
                )
                print(candidate)