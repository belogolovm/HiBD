import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base

conference_person = sql.Table('conference_person', Base.metadata,
    sql.Column('conference_id', sql.Integer, sql.ForeignKey('conference.id')),
    sql.Column('person_id', sql.Integer, sql.ForeignKey('person.id'))
)

class Conference(Base):
    __tablename__ = 'conference'

    id = sql.Column(sql.Integer, autoincrement=True, primary_key=True)

    name = sql.Column(sql.String(100), nullable=False)
    place = sql.Column(sql.String(100), nullable=False)
    date = sql.Column(sql.DateTime, nullable=False)

    participants = relationship('Person', secondary=conference_person)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'place': self.place,
            'date': self.date,
            'participants': [p.serialize() for p in self.participants]
        }