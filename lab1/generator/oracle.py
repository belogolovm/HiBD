import datetime
import sys

from lab1.model.oracle import OraclePerson, Rating, Group, LessonRecord
from .common import *
from ..model import databases
from sqlalchemy.orm import sessionmaker


def fill_oracle():
    print('Генерация данных в oracle...', end='')
    sys.stdout.flush()
    Session = sessionmaker(bind=databases['oracle']['engine'])
    session = Session()

    person_count = 50
    rating_count = person_count*5
    group_count = 5
    lessons_count = 20

    persons = []
    for i in range(person_count):
        p = OraclePerson()
        p.id = generate_person_id()
        p.name = generate_name()
        p.birth_date = generate_birthdate()

        p.country_id, p.country = generate_country()
        p.city_id, p.city = generate_city()
        p.city_id = p.country_id * 100 + p.city_id
        p.street_id, p.street = generate_street()
        p.street_id = p.city_id * 100 + p.street_id

        p.faculty = generate_faculty()
        p.position = generate_position()
        p.contract_from = datetime.datetime.now()
        p.contract_to = datetime.datetime.now()
        session.add(p)
        persons.append(p)

    for i in range(rating_count):
        r = Rating()
        r.discipline = generate_discipline()
        r.rating, r.rating_letter = generate_rating()
        r.date = generate_date()
        r.student = random.choice(persons)
        session.add(r)

    groups = []
    for i in range(group_count):
        g = Group()
        g.name = generate_group()
        g.study_type = generate_study_type()
        g.school = generate_school()
        g.direction = generate_specialty()
        g.speciality = generate_specialty()
        g.qualification = generate_qualification()
        g.study_year = "2019/2020"
        session.add(g)
        groups.append(g)

    for p in persons:
        group = random.choice(groups)
        group.students.append(p)


    for i in range(lessons_count):
        l = LessonRecord()
        l.name = generate_discipline()
        l.teacher = random.choice(persons)
        l.weekday = generate_weekday()
        l.hour = generate_hour()
        l.minute = generate_minute()
        l.room = generate_room()
        l.groups.append(random.choice(groups))
        session.add(l)

    session.commit()
    print('ОК')