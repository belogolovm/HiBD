import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base

conference_person = sql.Table('f_conference_person', Base.metadata,
    sql.Column('conference_id', sql.Integer, sql.ForeignKey('f_conference.id')),
    sql.Column('person_id', sql.Integer, sql.ForeignKey('f_person.id'))
)

class Conference(Base):
    __tablename__ = 'f_conference'

    id = sql.Column(sql.Integer, sql.Sequence('f_conference_seq_id'), primary_key=True)

    name = sql.Column(sql.String(100))
    place = sql.Column(sql.String(100))
    date_id = sql.Column(sql.Date, sql.ForeignKey('f_time.id'))
    date = relationship('FinalTime')

    participants = relationship('Person', secondary=conference_person)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'place': self.place,
            'date': self.date,
            'participants': [p.serialize() for p in self.participants]
        }