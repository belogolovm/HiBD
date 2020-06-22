import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base

lesson_group = sql.Table('f_lesson_group', Base.metadata,
    sql.Column('group_id', sql.Integer, sql.ForeignKey('f_group.id')),
    sql.Column('lesson_record_id', sql.Integer, sql.ForeignKey('f_lesson_record.id'))
)


class LessonRecord(Base):
    __tablename__ = 'f_lesson_record'

    id = sql.Column(sql.Integer, sql.Sequence('f_lesson_record_seq_id'), primary_key=True)

    name = sql.Column(sql.String(200), nullable=False)
    teacher_id = sql.Column(sql.Integer, sql.ForeignKey('f_person.id'), nullable=False)
    teacher = relationship('Person')
    weekday = sql.Column(sql.Integer)
    hour = sql.Column(sql.Integer)
    minute = sql.Column(sql.Integer)
    room = sql.Column(sql.String(10))
    groups = relationship('Group', secondary=lesson_group)

    def serialize(self):
        return {
            'name': self.name,
            'teacher': self.teacher.serialize(),
            'weekday': self.weekday,
            'hour': self.hour,
            'minute': self.minute,
            'room': self.room,
            'groups': [g.serialize() for g in self.groups],
        }