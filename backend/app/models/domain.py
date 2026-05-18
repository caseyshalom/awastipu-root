from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.core.database import Base

class ScamReport(Base):
    __tablename__ = "scam_reports"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True, nullable=True)
    bank_account = Column(String, index=True, nullable=True)
    scam_category = Column(String)
    description = Column(String)
    evidence_url = Column(String, nullable=True)
    reporter_alias = Column(String, nullable=True)
    risk_score = Column(Float, default=25.0)
    report_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
