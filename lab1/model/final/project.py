import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base

project_person = sql.Table('f_project_person', Base.metadata,
    sql.Column('project_id', sql.Integer, sql.ForeignKey('f_project.id')),
    sql.Column('person_id', sql.Integer, sql.ForeignKey('f_person.id'))
)

class Project(Base):
    __tablename__ = 'f_project'

    id = sql.Column(sql.Integer, sql.Sequence('f_project_seq_id'), primary_key=True)

    name = sql.Column(sql.String(100))
    date_from = sql.Column(sql.DateTime)
    date_to = sql.Column(sql.DateTime)

    participants = relationship('Person', secondary=project_person)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'participants': [p.serialize() for p in self.participants]
        }