import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base

publication_person = sql.Table('f_publication_person', Base.metadata,
    sql.Column('publication_id', sql.Integer, sql.ForeignKey('f_publication.id')),
    sql.Column('person_id', sql.Integer, sql.ForeignKey('f_person.id'))
)

class Publication(Base):
    __tablename__ = 'f_publication'

    id = sql.Column(sql.Integer, sql.Sequence('f_publication_seq_id'), primary_key=True)

    name = sql.Column(sql.String(300))
    language = sql.Column(sql.String(100))

    country = sql.Column(sql.String(100))
    country_id = sql.Column(sql.Integer)
    city = sql.Column(sql.String(100))
    city_id = sql.Column(sql.Integer)
    office = sql.Column(sql.String(100))
    office_id = sql.Column(sql.Integer)

    pages = sql.Column(sql.Integer)
    type = sql.Column(sql.String(100))
    quote_index = sql.Column(sql.Float)
    date_id = sql.Column(sql.DateTime, sql.ForeignKey('f_time.id'))
    date = relationship('FinalTime')

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