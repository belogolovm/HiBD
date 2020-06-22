import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base



class Person(Base):
    __tablename__ = 'person'

    id = sql.Column(sql.Integer, autoincrement=True, primary_key=True)

    name = sql.Column(sql.String(100), nullable=False)
    position = sql.Column(sql.String(100), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position
        }