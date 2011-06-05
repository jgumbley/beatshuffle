from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, MetaData
from sqlalchemy.orm import sessionmaker, mapper, relation 
from datetime import datetime
from sqlalchemy.sql import select
from flaskext.sqlalchemy import SQLAlchemy

# http://forge.mysql.com/wiki/TagSchema

db = SQLAlchemy()

meta = MetaData()
#engine = create_engine('postgresql://tnz_layer:c0ns0le@localhost:5432/tnz')
#Session=sessionmaker(bind=engine)

mix_table = Table(
        'tn', meta,
        Column('hash', String(length=None),  primary_key=True, nullable=False),
        )

link_table = Table('tn_tag', meta,
    Column('tn_hash', String(length=None), ForeignKey('tn.hash')),
    Column('tag_name', String(75), ForeignKey('tag.name')),
)

tag_table = Table('tag', meta,
    Column('name', String(75), primary_key=True),
)

class Mix(object):
    """Python class representing a mix, mapped to database entity
    """
    def __init__(self, hash):
        self.tags = []
        self.hash = hash

    def add_tag(self, _tag):
        self.tags.append(
                self._find_or_create_tag(_tag)
                )

    def _find_or_create_tag(self, tag):
        q = db.session.query(Tag).filter_by(name=tag)
        t = q.first()
        if not(t):
            t = Tag(tag)
        return t

    def list_of_tags(self):
        string = ""
        for tag in self.tags:
            string = string + tag + ":"
        return string[:-1]

    def __repr__(self):
        return self.hash 

class Tag(object):
    """Python class representing a Tag, mapped to a database entity
    """
    def __init__(self, tag):
        self.name = tag

mapper(Tag, tag_table)

mapper(Mix, mix_table, properties={
        'tags': relation(Tag, secondary=link_table, backref='tnz')
        })

#session = Session()

#def add_mix(mix):
#    session.add(mix)
#    session.commit()
    
