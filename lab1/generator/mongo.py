import datetime
import sys

from lab1.model.mongo import Dormitory, Person, Room, DormitoryPerson
from .common import *
from mongoengine import *

def fill_mongo():
    print('Генерация данных в mongodb...', end='')
    sys.stdout.flush()

    dormitory_count = 5
    room_count = 200
    person_count = 100

    dormitories = []
    for i in range(dormitory_count):
        d = Dormitory()
        d.name = generate_dormitory()
        d.total_rooms = generate_room()
        d.save()
        dormitories.append(d)

    rooms = []
    for i in range(room_count):
        r = Room()
        r.dormitory = random.choice(dormitories)
        r.room_number = str(generate_room() % r.dormitory.total_rooms)
        r.max_person = generate_max_person()
        r.insects = generate_bool()
        r.latest_debug = generate_date()
        r.save()
        rooms.append(r)

    for i in range(person_count):
        p = Person()
        p.person_id = generate_person_id()
        p.name = generate_name()
        p.is_beneficiary = generate_bool()
        p.is_contract_student = generate_bool()
        p.save()
        d = DormitoryPerson()
        d.person = p
        d.warnings = generate_warnings()
        d.room = random.choice(rooms)
        d.price = 500
        d.lives_from = generate_date()
        d.lives_to = generate_date()
        d.save()



    print('ОК')