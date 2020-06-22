import datetime
import sys

from sqlalchemy.orm import sessionmaker

from lab1.model import databases

from lab1.model.final.time import FinalTime

from lab1.model.oracle.oracleperson import OraclePerson
from lab1.model.final.person import Person as FinalPerson
from lab1.model.mongo.person import Person as MongoPerson
from lab1.model.mysql.person import Person as MySQLPerson

from lab1.model.mysql.conference import Conference as MySQLConference
from lab1.model.final.conference import Conference as FinalConference

from lab1.model.postgres.discipline import Discipline as PostgreDiscipline
from lab1.model.final.discipline import Discipline as FinalDiscipline

from lab1.model.mongo.dormitory import Dormitory as MongoDormitory
from lab1.model.final.dormitory import Dormitory as FinalDormitory

from lab1.model.mongo.room import Room as MongoRoom
from lab1.model.final.room import Room as FinalRoom

from lab1.model.mongo.dormitory_person import DormitoryPerson as MongoDormitoryPerson
from lab1.model.final.dormitory_person import DormitoryPerson as FinalDormitoryPerson

from lab1.model.oracle.group import Group as OracleGroup
from lab1.model.final.group import Group as FinalGroup

from lab1.model.oracle.lesson_record import LessonRecord as OracleLessonRecord
from lab1.model.final.lesson_record import LessonRecord as FinalLessonRecord

from lab1.model.mysql.library_record import LibraryRecord as MySQLLibRecord
from lab1.model.final.library_record import LibraryRecord as FinalLibRecord

from lab1.model.mysql.project import Project as MySQLProject
from lab1.model.final.project import Project as FinalProject

from lab1.model.mysql.publication import Publication as MySQLPublication
from lab1.model.final.publication import Publication as FinalPublication

from lab1.model.postgres.rating import Rating as PostgresRating
from lab1.model.oracle.rating import Rating as OracleRating
from lab1.model.final.rating import Rating as FinalRating


def create_time(session, id):
    t = session.query(FinalTime).filter_by(id=id).first()
    if t is None:
        t = FinalTime()
        t.id = id
        t.year = id.year
        t.year_id = id.year
        t.term = 1 if id.month <= 6 else 2
        t.term_id = t.year_id * 10 + t.term
        if t.term == 1:
            t.term = "весенний"
            t.end_term = datetime.date(id.year, 6, 30)
        else:
            t.term = "осенний"
            t.end_term = datetime.date(id.year, 12, 31)
        t.end_year = datetime.date(id.year, 12, 31)
        session.add(t)
    return t
    

def migrate_all():
    print('Миграция данных о людях...', end='')
    sys.stdout.flush()

    Session = sessionmaker(bind=databases['oracle']['engine'])
    session_oracle = Session()

    Session = sessionmaker(bind=databases['mysql']['engine'])
    session_mysql = Session()

    Session = sessionmaker(bind=databases['postgres']['engine'])
    session_postgres = Session()

    # Oracle -> Oracle
    for p in session_oracle.query(OraclePerson).all():
        statement = FinalPerson()
        statement.id = p.id
        statement.name = p.name
        statement.position = p.position

        statement.country_id = p.country_id
        statement.country = p.country
        statement.city_id = p.city_id
        statement.city = p.city
        statement.street_id = p.street_id
        statement.street = p.street

        statement.birth_date = create_time(session_oracle, p.birth_date)

        statement.faculty = p.faculty
        statement.contract_from = p.contract_from
        statement.contract_to = p.contract_to
        session_oracle.add(statement)

    # Postgres -> Oracle
    for m in session_postgres.query(PostgresRating).all():
        statement = session_oracle.query(FinalPerson).filter_by(id=m.student_id).first()
        if statement is None:
            statement = FinalPerson()
            statement.id = m.student_id
            statement.name = m.student_name
            session_oracle.add(statement)
        statement = session_oracle.query(FinalPerson).filter_by(id=m.teacher_id).first()
        if statement is None:
            statement = FinalPerson()
            statement.id = m.teacher_id
            statement.name = m.teacher_name
            session_oracle.add(statement)

    # Mongo -> Oracle
    for m in MongoPerson.objects():
        statement = session_oracle.query(FinalPerson).filter_by(id=m.person_id).first()
        if statement is None:
            # Информации нет, создаём
            statement = FinalPerson()
            statement.id = m.person_id
            statement.name = m.name
            statement.is_beneficiary = m.is_beneficiary
            statement.is_contract_student = m.is_contract_student
            session_oracle.add(statement)
        else:
            statement.is_beneficiary = m.is_beneficiary
            statement.is_contract_student = m.is_contract_student


    # MySQL -> Oracle
    for m in session_mysql.query(MySQLPerson).all():
        statement = session_oracle.query(FinalPerson).filter_by(id=m.id).first()
        if statement is None:
            # Информации нет, создаём
            statement = FinalPerson()
            statement.id = m.id
            statement.name = m.name
            statement.position = m.position
            session_oracle.add(statement)
        else:
            # Если не заполнено, заполняем
            if statement.position is None:
                statement.position = m.position

    session_oracle.commit()
    print('ОК')

    print('Миграция данных о конференциях...', end='')
    sys.stdout.flush()

    for c in session_mysql.query(MySQLConference).all():
        statement = FinalConference()
        statement.id = c.id
        statement.name = c.name
        statement.place = c.place

        statement.date = create_time(session_oracle, c.date)

        for p in c.participants:
            statement.participants.append(session_oracle.query(FinalPerson).filter_by(id=p.id).first())
        session_oracle.add(statement)

    session_oracle.commit()
    print('ОК')

    print('Миграция данных о дисциплинах...', end='')
    sys.stdout.flush()

    # Postgres -> Oracle
    for p in session_postgres.query(PostgreDiscipline).all():
        statement = FinalDiscipline()
        statement.university_name = p.university_name
        statement.standard = p.standard
        statement.name = p.name
        statement.faculty = p.faculty
        statement.specialty = p.specialty
        statement.term = p.term
        statement.lecture_hours = p.lecture_hours
        statement.practice_hours = p.practice_hours
        statement.laboratory_hours = p.laboratory_hours
        statement.is_exam = p.is_exam
        session_oracle.add(statement)

    # Oracle -> Oracle
    for r in session_oracle.query(OracleRating).all():
        statement = session_oracle.query(FinalDiscipline).filter_by(name=r.discipline).first()
        if statement is None:
            statement = FinalDiscipline()
            statement.name = r.discipline
            session_oracle.add(statement)

    session_oracle.commit()
    print('ОК')

    print('Миграция данных об общежитиях...', end='')
    sys.stdout.flush()

    # Mongo -> Oracle
    for d in MongoDormitory.objects():
        statement = FinalDormitory()
        statement.name = d.name
        statement.total_rooms = d.total_rooms
        session_oracle.add(statement)

    session_oracle.commit()
    print('ОК')

    print('Миграция данных о комнатах в общежитиях...', end='')
    sys.stdout.flush()

    # Mongo -> Oracle
    for r in MongoRoom.objects():
        statement = FinalRoom()
        statement.room_number = r.room_number
        statement.insects = r.insects
        statement.max_person = r.max_person
        statement.latest_debug = r.latest_debug
        statement.dormitory = session_oracle.query(FinalDormitory).filter_by(name=r.dormitory.name, total_rooms=r.dormitory.total_rooms).first()
        session_oracle.add(statement)

    session_oracle.commit()
    print('ОК')
    
    print('Миграция данных о жителях общежитий...', end='')
    sys.stdout.flush()

    # Mongo -> Oracle
    for p in MongoDormitoryPerson.objects():
        statement = FinalDormitoryPerson()
        statement.warnings = p.warnings
        statement.room = session_oracle.query(FinalRoom).filter_by(room_number=p.room.room_number, max_person=p.room.max_person).first()
        statement.price = p.price

        statement.lives_from = create_time(session_oracle, p.lives_from)
        statement.lives_to = create_time(session_oracle, p.lives_to)

        statement.person = session_oracle.query(FinalPerson).filter_by(id=p.person.person_id).first()
        session_oracle.add(statement)

    session_oracle.commit()
    print('ОК')

    print('Миграция данных о группах...', end='')
    sys.stdout.flush()
    
    # Oracle -> Oracle
    for g in session_oracle.query(OracleGroup).all():
        statement = FinalGroup()
        statement.id = g.id
        statement.name = g.name
        statement.study_type = g.study_type
        statement.school = g.school
        statement.direction = g.direction
        statement.speciality = g.speciality
        statement.qualification = g.qualification
        statement.study_year = g.study_year
        for s in g.students:
            statement.students.append(session_oracle.query(FinalPerson).filter_by(id=s.id).first())
        session_oracle.add(statement)

    session_oracle.commit()
    print('ОК')
    
    print('Миграция раписания...', end='')
    sys.stdout.flush()
    
    # Oracle -> Oracle
    for r in session_oracle.query(OracleLessonRecord).all():
        statement = FinalLessonRecord()
        statement.name = r.name
        statement.teacher_id = r.teacher_id
        statement.weekday = r.weekday
        statement.hour = r.hour
        statement.minute = r.minute
        statement.room = r.room
        for g in r.groups:
            statement.groups.append(session_oracle.query(FinalGroup).filter_by(id=g.id).first())
        session_oracle.add(statement)

    session_oracle.commit()
    print('ОК')
    
    print('Миграция читательского листа...', end='')
    sys.stdout.flush()

    # MySQL -> Oracle
    for r in session_mysql.query(MySQLLibRecord).all():
        statement = FinalLibRecord()
        statement.book_name = r.book_name
        statement.taken_by_id = r.taken_by_id

        statement.taken_at = create_time(session_oracle, r.taken_at)
        statement.returned_at = create_time(session_oracle, r.returned_at)
        session_oracle.add(statement)
    
    session_oracle.commit()
    print('ОК')

    print('Миграция проектов...', end='')
    sys.stdout.flush()

    for r in session_mysql.query(MySQLProject).all():
        statement = FinalProject()
        statement.name = r.name
        statement.date_from = r.date_from
        statement.date_to = r.date_to
        for p in r.participants:
            statement.participants.append(session_oracle.query(FinalPerson).filter_by(id=p.id).first())
        session_oracle.add(statement)

    session_oracle.commit()
    print('ОК')

    print('Миграция публикаций...', end='')
    sys.stdout.flush()

    for r in session_mysql.query(MySQLPublication).all():
        statement = FinalPublication()
        statement.name = r.name
        statement.language = r.language
        statement.country = r.country
        statement.country_id = r.country_id
        statement.city = r.city
        statement.city_id = r.city_id
        statement.office = r.office
        statement.office_id = r.office_id
        statement.type = r.type
        statement.quote_index = r.quote_index
        statement.date = create_time(session_oracle, r.date)
        for p in r.authors:
            statement.authors.append(session_oracle.query(FinalPerson).filter_by(id=p.id).first())
        session_oracle.add(statement)

    session_oracle.commit()
    print('ОК')

    print('Миграция оценок...', end='')
    sys.stdout.flush()

    # Postgres -> Oracle
    for r in session_postgres.query(PostgresRating).all():
        statement = FinalRating()
        statement.discipline_id = r.discipline_id
        statement.rating = r.rating
        if statement.rating == '5':
            statement.rating_letter = 'A'
        elif statement.rating == '4':
            statement.rating_letter = 'B'
        elif statement.rating == '3':
            statement.rating_letter = 'D'
        else:
            statement.rating_letter = 'FX'
        statement.date = create_time(session_oracle, r.date)
        statement.teacher_id = r.teacher_id
        statement.student_id = r.student_id
        session_oracle.add(statement)
        session_oracle.commit()

    # Oracle -> Oracle
    for r in session_oracle.query(OracleRating).all():
        statement = FinalRating()
        statement.discipline_id = session_oracle.query(FinalDiscipline).filter_by(name=r.discipline).first().id
        statement.rating = r.rating
        statement.rating_letter = r.rating_letter
        statement.date = create_time(session_oracle, r.date)
        statement.student_id = r.student_id
        session_oracle.add(statement)

    session_oracle.commit()
    print('ОК')

    print('Создаём таблицы фактов...', end='')
    sys.stdout.flush()

    tables_to_drop = [
        'LAB_ORACLE_USER.FACT_1',
        'LAB_ORACLE_USER.FACT_2',
        'LAB_ORACLE_USER.FACT_3',
        'LAB_ORACLE_USER.FACT_4',
    ]

    for table in tables_to_drop:
        try:
            databases['oracle']['engine'].execute(f"drop table {table}")
        except:
            pass

    statements = [
        # Fact 3
        """
            create TABLE LAB_ORACLE_USER.FACT_3 as
            SELECT
                LAB_ORACLE_USER.F_PUBLICATION.ID PUBLICATION_ID,
                LAB_ORACLE_USER.F_PUBLICATION.DATE_ID,
                COUNT(LAB_ORACLE_USER.F_PERSON.ID) PERSONS
            FROM
                 LAB_ORACLE_USER.F_PUBLICATION,
                 LAB_ORACLE_USER.F_PERSON,
                 LAB_ORACLE_USER.F_PUBLICATION_PERSON
            where
                  LAB_ORACLE_USER.F_PERSON.ID = LAB_ORACLE_USER.F_PUBLICATION_PERSON.PERSON_ID
                  AND LAB_ORACLE_USER.F_PUBLICATION_PERSON.PUBLICATION_ID = LAB_ORACLE_USER.F_PUBLICATION.ID
            GROUP BY
                LAB_ORACLE_USER.F_PUBLICATION.ID,
                LAB_ORACLE_USER.F_PUBLICATION.DATE_ID
        """,
        # "ALTER TABLE LAB_ORACLE_USER.FACT_3 ADD CONSTRAINT FK_P FOREIGN KEY (PUBLICATION_ID) REFERENCES LAB_ORACLE_USER.F_PUBLICATION (ID);",
        # "ALTER TABLE LAB_ORACLE_USER.FACT_3 ADD CONSTRAINT FK_D FOREIGN KEY (DATE_ID) REFERENCES LAB_ORACLE_USER.F_TIME (ID);",

        """
            create TABLE LAB_ORACLE_USER.FACT_2 as
            SELECT
                LAB_ORACLE_USER.F_PERSON.STREET_ID,
                LAB_ORACLE_USER.F_PERSON.BIRTH_DATE_ID,
                COUNT(LAB_ORACLE_USER.F_PERSON.ID) PERSONS
            FROM
                 LAB_ORACLE_USER.F_TIME,
                 LAB_ORACLE_USER.F_PERSON
            where
                  LAB_ORACLE_USER.F_PERSON.BIRTH_DATE_ID = LAB_ORACLE_USER.F_TIME.ID
            GROUP BY
                LAB_ORACLE_USER.F_PERSON.STREET_ID,
                LAB_ORACLE_USER.F_PERSON.BIRTH_DATE_ID
        """,

        # "ALTER TABLE LAB_ORACLE_USER.FACT_2 ADD CONSTRAINT FK_FACT_2_D FOREIGN KEY (BIRTH_DATE_ID) REFERENCES LAB_ORACLE_USER.F_TIME (ID);",
    ]

    for statement in statements:
        databases['oracle']['engine'].execute(statement)
    print('ОК')