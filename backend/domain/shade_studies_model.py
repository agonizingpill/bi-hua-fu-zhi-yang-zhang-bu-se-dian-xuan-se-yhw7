from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


shade_studies = Table('shade_studies', metadata,
    Column('code', String(64), primary_key=True),
    Column('panel', String(160), ForeignKey('proof_regions.code'), nullable=False),
    Column('revision', Integer, nullable=False),
    Column('x_mm', Integer, nullable=False),
    Column('y_mm', Integer, nullable=False),
    Column('ground_l', Float, nullable=False),
    Column('fraction', Float, nullable=False),
    Column('mean_de', Float, nullable=False),
    Column('lower_de', Float, nullable=False),
    Column('upper_de', Float, nullable=False),
    Column('test_mae', Float, nullable=False),
    Column('token', String(64), nullable=False, unique=True),
    CheckConstraint('x_mm >= 0'),
    CheckConstraint('y_mm >= 0'),
    CheckConstraint('fraction BETWEEN 0 AND 1'),
    CheckConstraint('0 <= lower_de AND lower_de <= mean_de AND upper_de >= mean_de'),
)
