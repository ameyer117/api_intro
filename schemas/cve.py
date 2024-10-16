# schemas.py
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from typing import Optional

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"

class CVEBase(BaseModel):
    cve_id: str
    description: str
    severity: Severity
    published_date: datetime

class CVECreation(BaseModel):
    cve_id: str
    description: str
    severity: Severity
    published_date: datetime

class CVEUpdate(BaseModel):
    cve_id: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[Severity] = None
    published_date: Optional[datetime] = None

class CVEInDB(CVEBase):

    class Config:
        from_attributes = True
