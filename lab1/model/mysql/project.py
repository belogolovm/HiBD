import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base

project_person = sql.Table('project_person', Base.metadata,
    sql.Column('project_id', sql.Integer, sql.ForeignKey('project.id')),
    sql.Column('person_id', sql.Integer, sql.ForeignKey('person.id'))
)

class Project(Base):
    __tablename__ = 'project'

    id = sql.Column(sql.Integer, autoincrement=True, primary_key=True)

    name = sql.Column(sql.String(100), nullable=False)
    date_from = sql.Column(sql.DateTime, nullable=False)
    date_to = sql.Column(sql.DateTime, nullable=False)

    participants = relationship('Person', secondary=project_person)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'participants': [p.serialize() for p in self.participants]
        }