from sqlalchemy import CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


# 整碗签认：一碗颜料对应同一张样张上的一组补色点，全组共用一个调色比例
color_bowls = Table('color_bowls', metadata,
    Column('code', String(48), primary_key=True),
    Column('panel', String(160), ForeignKey('proof_regions.code'), nullable=False),
    Column('revision', Integer, nullable=False),
    Column('fraction', Float, nullable=False),
    Column('mean_de', Float, nullable=False),
    Column('lower_de', Float, nullable=False),
    Column('upper_de', Float, nullable=False),
    Column('max_upper_de', Float, nullable=False),
    Column('test_mae', Float, nullable=False),
    Column('token', String(64), nullable=False, unique=True),
    Column('points', JSON, nullable=False),
    CheckConstraint('fraction BETWEEN 0 AND 1'),
    CheckConstraint('revision >= 1'),
    CheckConstraint('0 <= lower_de AND lower_de <= mean_de AND upper_de >= mean_de'),
    CheckConstraint('max_upper_de >= upper_de'),
)


# 整碗领位回执：以客户端请求键做主键，保证同一领位请求重试取回原组、不重复占位
bowl_claims = Table('bowl_claims', metadata,
    Column('claim_key', String(160), primary_key=True),
    Column('bowl', String(48), ForeignKey('color_bowls.code'), nullable=False),
    Column('reader', String(160), nullable=False),
)
