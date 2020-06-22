import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base

publication_person = sql.Table('publication_person', Base.metadata,
    sql.Column('publication_id', sql.Integer, sql.ForeignKey('publication.id')),
    sql.Column('person_id', sql.Integer, sql.ForeignKey('person.id'))
)

class Publication(Base):
    __tablename__ = 'publication'

    id = sql.Column(sql.Integer, autoincrement=True, primary_key=True)

    name = sql.Column(sql.String(300), nullable=False)
    language = sql.Column(sql.String(100), nullable=False)

    country_id = sql.Column(sql.Integer, nullable=False)
    country = sql.Column(sql.String(100), nullable=False)
    city = sql.Column(sql.String(100), nullable=False)
    city_id = sql.Column(sql.Integer, nullable=False)
    office = sql.Column(sql.String(100), nullable=False)
    office_id = sql.Column(sql.Integer, nullable=False)

    pages = sql.Column(sql.Integer, nullable=False)
    type = sql.Column(sql.String(100), nullable=False)
    quote_index = sql.Column(sql.Float, nullable=False)
    date = sql.Column(sql.DateTime, nullable=False)

    authors = relationship('Person', secondary=publication_person)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'source': self.source,
            'pages': self.pages,
            'place': self.place,
            'type': self.type,
            'quote_index': self.quote_index,
            'date': self.date,
            # 'authors': [a.serialize() for a in self.authors],
        }