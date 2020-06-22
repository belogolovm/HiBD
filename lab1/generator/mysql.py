import datetime
import sys

from lab1.model.mysql import Person, Conference, Publication, Project, LibraryRecord
from .common import *
from ..model import databases
from sqlalchemy.orm import sessionmaker


def fill_mysql():
    print('Генерация данных в mysql...', end='')
    sys.stdout.flush()
    Session = sessionmaker(bind=databases['mysql']['engine'])
    session = Session()

    person_count = 50
    conference_count = 5
    publication_count = 100
    project_count = 10
    library_records = 500

    persons = []
    for i in range(person_count):
        p = Person()
        p.id = generate_person_id()
        p.name = generate_name()
        p.position = generate_position()
        session.add(p)
        persons.append(p)

    for i in range(conference_count):
        c = Conference()
        c.name = generate_conference()
        c.place = generate_place()
        c.date = generate_date()
        for p in random.choices(persons, k=random.randrange(person_count)):
            c.participants.append(p)

        session.add(c)

    for i in range(publication_count):
        p = Publication()
        p.name = generate_publication_name()
        p.language = generate_language()

        p.country_id, p.country = generate_country()
        p.city_id, p.city = generate_city()
        p.city_id = p.country_id * 100 + p.city_id
        p.office_id, p.office = generate_office()
        p.office = f'{p.office}, г.{p.city}'
        p.office_id = p.city_id * 100 + p.office_id

        p.pages = generate_pages()
        p.type = generate_publication_type()
        p.date = generate_date()
        p.quote_index = generate_quote_index()
        for a in random.choices(persons, k=random.randrange(3)):
            p.authors.append(a)

        session.add(p)

    for i in range(project_count):
        p = Project()
        p.name = generate_project_name()
        p.date_from = generate_date()
        p.date_to = generate_date()
        for person in random.choices(persons, k=random.randrange(10)):
            p.participants.append(person)

        session.add(p)

    for i in range(library_records):
        record1 = LibraryRecord()
        record1.book_name = generate_book_name()
        record1.taken_by = random.choice(persons)
        record1.taken_at = generate_date()
        record1.returned_at = generate_date()
        session.add(record1)

    session.commit()
    print('ОК')