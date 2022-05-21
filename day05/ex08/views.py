from django.conf import settings
from django.http import HttpRequest, HttpResponse
import psycopg2
import os
import path
from django.shortcuts import render, redirect


def init(request):
    try:
        conn = psycopg2.connect(
            "dbname={} user={} password={} host={} port={}".format(
                settings.DATABASES['default']['NAME'],
                settings.DATABASES['default']['USER'],
                settings.DATABASES['default']['PASSWORD'],
                settings.DATABASES['default']['HOST'],
                settings.DATABASES['default']['PORT']))

        sql1 = """CREATE TABLE IF NOT EXISTS ex08_planets (
            id SERIAL PRIMARY KEY,
            name VARCHAR(64) UNIQUE NOT NULL,
            climate VARCHAR,
            diameter integer,
            orbital_period INT,
            population BIGINT,
            rotation_period INT,
            surface_water real,
            terrain VARCHAR(128)
            );"""

        sql2 = """CREATE TABLE IF NOT EXISTS ex08_people (
            id SERIAL PRIMARY KEY,
            name VARCHAR(64) UNIQUE NOT NULL,
            birth_year VARCHAR(32),
            gender VARCHAR(32),
            eye_color VARCHAR(32),
            hair_color VARCHAR(32),
            height INT,
            mass real,
            homeworld VARCHAR(64) REFERENCES ex08_planets(name)
            );"""
        with conn.cursor() as curs:
            curs.execute(sql1)
            curs.execute('COMMIT')
            curs.execute(sql2)
            curs.execute('COMMIT')

        return HttpResponse("OK")

    except psycopg2.Error as e:
        print(HttpRequest())
        return HttpResponse(e)


def populate(request):
    conn = psycopg2.connect(
        "dbname={} user={} password={} host={} port={}".format(
            settings.DATABASES['default']['NAME'],
            settings.DATABASES['default']['USER'],
            settings.DATABASES['default']['PASSWORD'],
            settings.DATABASES['default']['HOST'],
            settings.DATABASES['default']['PORT']))
    module_dir = path.Path(os.path.dirname(__file__))
    planets_path = module_dir / 'static/planets.csv'
    people_path = module_dir / 'static/people.csv'
    planets_data = planets_path.open("r")
    people_data = people_path.open("r")
    cur = conn.cursor()
    result = []
    try:
        cur.copy_from(planets_data, 'ex08_planets', columns=(
            'name', 'climate', 'diameter', 'orbital_period', 'population',
            'rotation_period', 'surface_water', 'terrain'), null='NULL')
        conn.commit()
        result = ['planets -> OK<br>']
    except psycopg2.DatabaseError as e:
        conn.rollback()
        result.append(e)
        result.append("<br>")
    try:
        cur.copy_from(people_data, 'ex08_people', columns=(
            'name', 'birth_year', 'gender', 'eye_color', 'hair_color', 'height',
            'mass', 'homeworld'), null='NULL')
        conn.commit()
        result.append('people -> OK')
    except psycopg2.DatabaseError as e:
        conn.rollback()
        result.append(e)
        result.append("<br>")
    return HttpResponse(result)


def display(request):
    try:
        conn = psycopg2.connect(
            "dbname={} user={} password={} host={} port={}".format(
                settings.DATABASES['default']['NAME'],
                settings.DATABASES['default']['USER'],
                settings.DATABASES['default']['PASSWORD'],
                settings.DATABASES['default']['HOST'],
                settings.DATABASES['default']['PORT']))
        with conn.cursor() as curs:
            curs.execute(
                """
            select ex08_people.name,homeworld,ex08_planets.climate
            from ex08_people 
            right join ex08_planets on ex08_people.homeworld = ex08_planets.name
            where ex08_planets.climate like '%windy%' 
            order by ex08_people.name;
            """)
            people = curs.fetchall()
            if not people:
                raise
        return render(request, 'ex08/display.html', {"people": people})
    except Exception as e:
        return HttpResponse("No data available")
