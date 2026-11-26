from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


patch_slots = Table('patch_slots', metadata,
    Column('code', String(64), primary_key=True),
    Column('panel', String(160), ForeignKey('proof_regions.code'), nullable=False),
    Column('study', String(160), ForeignKey('shade_studies.code'), nullable=False, unique=True),
    Column('x_mm', Integer, nullable=False),
    Column('y_mm', Integer, nullable=False),
    Column('site_key', String(160), nullable=False, unique=True),
    Column('reader', String(160), nullable=False),
    Column('delta_seen', Float, nullable=True),
    Column('receipt', String(160), nullable=True, unique=True),
    Column('state', String(160), nullable=False),
    CheckConstraint('x_mm >= 0'),
    CheckConstraint('y_mm >= 0'),
    CheckConstraint("state IN ('已领取','待复样','已消费')"),
)
