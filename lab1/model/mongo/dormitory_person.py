from mongoengine import *

from lab1.model.mongo.person import Person
from lab1.model.mongo.room import Room


class DormitoryPerson(Document):
    person = ReferenceField(Person)
    warnings = DecimalField(default=0)
    room = ReferenceField(Room)
    price = DecimalField(required=True)
    lives_from = DateField(required=True)
    lives_to = DateField(required=True)
