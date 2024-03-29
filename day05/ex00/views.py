from django.conf import settings
from django.http import HttpRequest, HttpResponse
import psycopg2


def init(request):
    try:
        conn = psycopg2.connect("dbname={} user={} password={} host={} port={}".format(
            settings.DATABASES['default']['NAME'],
            settings.DATABASES['default']['USER'],
            settings.DATABASES['default']['PASSWORD'],
            settings.DATABASES['default']['HOST'],
            settings.DATABASES['default']['PORT']))

        sql = """CREATE TABLE IF NOT EXISTS ex00_movies (
            title char(64) UNIQUE NOT NULL,
            episode_nb INT PRIMARY KEY,
            opening_crawl TEXT,
            director VARCHAR(32) NOT NULL,
            producer VARCHAR(128) NOT NULL,
            release_date DATE NOT NULL
            );"""
        with conn.cursor() as curs:
            curs.execute(sql)
            curs.execute('COMMIT')

        return HttpResponse("OK")

    except psycopg2.Error as e:
        return HttpResponse(e, status=500)

