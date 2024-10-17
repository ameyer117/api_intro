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
    cve_id: str = Field(..., pattern=r'^CVE-\d{4}-\d{4,}$', description="CVE ID in the format CVE-YYYY-NNNN",examples=["CVE-2023-12345"])
    description: str = Field(..., max_length=10000, description="Detailed description of the vulnerability (max 10,000 characters)", examples=["This is a vulnerability description"])
    severity: Severity
    published_date: datetime

class CVEUpdate(BaseModel):
    cve_id: str = Field(..., pattern=r'^CVE-\d{4}-\d{4,}$', description="CVE ID in the format CVE-YYYY-NNNN",examples=["CVE-2023-12345"])
    description: Optional[str] = Field(None, max_length=10000, description="Detailed description of the vulnerability (max 10,000 characters)", examples=["This is a vulnerability description"])
    severity: Optional[Severity] = None
    published_date: Optional[datetime] = None

class CVEInDB(CVEBase):

    class Config:
        from_attributes = True
