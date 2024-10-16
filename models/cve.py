# models.py

from sqlalchemy import Column, Integer, String, Text
from database import Base

class CVE(Base):
    __tablename__ = "cves"

    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String, nullable=False)  # e.g., Low, Medium, High, Critical
    published_date = Column(String, nullable=False)  # ISO format date string
