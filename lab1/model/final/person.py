import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base


class Person(Base):
    __tablename__ = 'f_person'

    id = sql.Column(sql.Integer, primary_key=True)

    name = sql.Column(sql.String(100))
    position = sql.Column(sql.String(100))

    birth_date_id = sql.Column(sql.Date, sql.ForeignKey('f_time.id'))
    birth_date = relationship('FinalTime')

    country = sql.Column(sql.String(100))
    country_id = sql.Column(sql.Integer)
    city = sql.Column(sql.String(100))
    city_id = sql.Column(sql.Integer)
    street = sql.Column(sql.String(100))
    street_id = sql.Column(sql.Integer)

    faculty = sql.Column(sql.String(100))

    contract_from = sql.Column(sql.Date)
    contract_to = sql.Column(sql.Date)

    is_beneficiary = sql.Column(sql.Boolean)
    is_contract_student = sql.Column(sql.Boolean)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'birth_date': self.birth_date,
            'birth_place': self.birth_place,
            'faculty': self.faculty,
            'contract_from': self.contract_from,
            'contract_to': self.contract_to,
            'is_beneficiary': self.is_beneficiary,
            'is_contract_student': self.is_contract_student

        }