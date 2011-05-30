from sqlalchemy import *
from migrate import *

meta = MetaData()

mix_table = Table(
        'tn', meta,
        Column('hash', String(length=None),  primary_key=True, nullable=False),
        )

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    mix_table.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    mix_table.drop()
