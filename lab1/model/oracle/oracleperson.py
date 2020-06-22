import sqlalchemy as sql
from sqlalchemy.orm import relationship

from lab1.model.mysql.project import project_person
from . import Base


class OraclePerson(Base):
    __tablename__ = 'oracle_person'

    id = sql.Column(sql.Integer, primary_key=True)

    name = sql.Column(sql.String(100), nullable=False)
    position = sql.Column(sql.String(100), nullable=False)
    birth_date = sql.Column(sql.Date, nullable=False)
    faculty = sql.Column(sql.String(100), nullable=False)

    country = sql.Column(sql.String(100))
    country_id = sql.Column(sql.Integer)
    city = sql.Column(sql.String(100))
    city_id = sql.Column(sql.Integer)
    street = sql.Column(sql.String(100))
    street_id = sql.Column(sql.Integer)

    contract_from = sql.Column(sql.Date, nullable=False)
    contract_to = sql.Column(sql.Date, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'birth_date': self.birth_date,
            'birth_place': self.birth_place,
            'faculty': self.faculty,
            'position': self.position,
            'contract_from': self.contract_from,
            'contractTo': self.contract_to,
        }