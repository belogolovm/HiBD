from mongoengine import *

from lab1.model.mongo.dormitory import Dormitory


class Room(Document):
    dormitory = ReferenceField(Dormitory)
    room_number = StringField(required=True)
    insects = BooleanField(default=0)
    max_person = DecimalField(required=True)
    latest_debug = DateField(default=0)
