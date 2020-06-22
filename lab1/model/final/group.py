import sqlalchemy as sql
from sqlalchemy.orm import relationship

from lab1.model.mysql.project import project_person
from . import Base

group_person = sql.Table('f_group_person', Base.metadata,
    sql.Column('group_id', sql.Integer, sql.ForeignKey('f_group.id')),
    sql.Column('person_id', sql.Integer, sql.ForeignKey('f_person.id'))
)

class Group(Base):
    __tablename__ = 'f_group'

    id = sql.Column(sql.Integer, sql.Sequence('f_group_seq_id'), primary_key=True)

    name = sql.Column(sql.String(100))
    study_type = sql.Column(sql.String(200))
    school = sql.Column(sql.String(200))
    direction = sql.Column(sql.String(200))
    speciality = sql.Column(sql.String(200))
    qualification = sql.Column(sql.String(200))
    study_year = sql.Column(sql.String(10))
    students = relationship('Person', secondary=group_person)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'study_type': self.study_type,
            'school': self.school,
            'direction': self.direction,
            'speciality': self.speciality,
            'qualification': self.qualification,
            'study_year': self.study_year,
            'students': [s.serialize() for s in self.students]
        }