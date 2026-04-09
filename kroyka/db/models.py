from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from kroyka.db.session import Base

class CutJob(Base):
    __tablename__ = 'cut_jobs'
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(36), unique=True, index=True, nullable=False)
    status = Column(String(20), default='pending', nullable=False)
    cnc_type = Column(String(20), default='holzma')
    kerf = Column(Float, default=3.2)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    parts_json = Column(JSON, nullable=True)
    result_json = Column(JSON, nullable=True)
    errors_json = Column(JSON, nullable=True)

class StockSheet(Base):
    __tablename__ = 'stock_sheets'
    id = Column(Integer, primary_key=True, index=True)
    material = Column(String(100), nullable=False, index=True)
    length = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    thickness = Column(Float, default=16.0)
    qty = Column(Integer, default=1)
    grain = Column(Boolean, default=False)
    cost_per_sheet = Column(Float, default=0.0)
    supplier = Column(String(200), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class Material(Base):
    __tablename__ = 'materials'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    thickness = Column(Float, default=16.0)
    cost_per_sqm = Column(Float, default=0.0)
    kerf_default = Column(Float, default=3.2)
    grain_sensitive = Column(Boolean, default=False)
