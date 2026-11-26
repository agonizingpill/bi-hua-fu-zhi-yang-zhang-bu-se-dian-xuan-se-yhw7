from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


proof_regions = Table('proof_regions', metadata,
    Column('code', String(64), primary_key=True),
    Column('label', String(160), nullable=False),
    Column('pigment_family', String(160), nullable=False),
    Column('width_mm', Integer, nullable=False),
    Column('height_mm', Integer, nullable=False),
    Column('frame_inset', Integer, nullable=False),
    Column('hold_x1', Integer, nullable=False),
    Column('hold_y1', Integer, nullable=False),
    Column('hold_x2', Integer, nullable=False),
    Column('hold_y2', Integer, nullable=False),
    Column('revision', Integer, nullable=False),
    CheckConstraint('width_mm > 0'),
    CheckConstraint('height_mm > 0'),
    CheckConstraint('frame_inset >= 0'),
    CheckConstraint('hold_x1 < hold_x2'),
    CheckConstraint('hold_y1 < hold_y2'),
    CheckConstraint('revision >= 1'),
)
