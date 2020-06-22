import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base


class DormitoryPerson(Base):
    __tablename__ = 'f_dorm_person'

    id = sql.Column(sql.Integer, sql.Sequence('f_dorm_person_seq_id'), primary_key=True)

    person_id = sql.Column(sql.Integer, sql.ForeignKey('f_person.id'))
    person = relationship('Person')
    warnings = sql.Column(sql.Integer)
    room_id = sql.Column(sql.Integer, sql.ForeignKey('f_room.id'))
    room = relationship('Room')
    price = sql.Column(sql.Integer)

    lives_from_id = sql.Column(sql.Date, sql.ForeignKey('f_time.id'))
    lives_from = relationship('FinalTime', foreign_keys=[lives_from_id])
    lives_to_id = sql.Column(sql.Date, sql.ForeignKey('f_time.id'))
    lives_to = relationship('FinalTime', foreign_keys=[lives_to_id])


    def serialize(self):
        return {
            'id': self.id,
            'person': self.person.serialize() if self.person is not None else None,
            'warnings': self.warnings,
            'room': self.room.serialize() if self.room is not None else None,
            'price': self.price,
            'lives_from': self.lives_from,
            'lives_to': self.lives_to
        }