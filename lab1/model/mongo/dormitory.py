from mongoengine import *


class Dormitory(Document):
    name = StringField(required=True, max_length=100)
    total_rooms = DecimalField()
