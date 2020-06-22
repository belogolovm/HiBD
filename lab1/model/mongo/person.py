from mongoengine import *


class Person(Document):
    person_id = DecimalField(required=True)
    name = StringField(required=True, max_length=200)
    is_beneficiary = BooleanField(required=True)
    is_contract_student = BooleanField(required=True)
