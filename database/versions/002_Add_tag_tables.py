from sqlalchemy import *
from migrate import *

meta = MetaData()

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

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    tag_table.create()
    link_table.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    link_table.drop()
    tag_table.drop()
