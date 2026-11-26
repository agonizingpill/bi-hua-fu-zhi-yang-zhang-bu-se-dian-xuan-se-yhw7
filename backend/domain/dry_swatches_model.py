from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


dry_swatches = Table('dry_swatches', metadata,
    Column('code', String(64), primary_key=True),
    Column('family', String(160), nullable=False),
    Column('fraction', Float, nullable=False),
    Column('ground_l', Float, nullable=False),
    Column('delta_e', Float, nullable=False),
    Column('sample_ref', String(160), nullable=False, unique=True),
    Column('dry_hours', Integer, nullable=False),
    Column('witnessed', Boolean, nullable=False),
    CheckConstraint('fraction BETWEEN 0 AND 1'),
    CheckConstraint('ground_l BETWEEN 0 AND 100'),
    CheckConstraint('delta_e >= 0'),
    CheckConstraint('dry_hours BETWEEN 0 AND 240'),
)
