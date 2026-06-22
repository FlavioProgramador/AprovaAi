from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    edital_id = Column(Integer, ForeignKey("editais.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    weight = Column(String, nullable=False)
    relevance_percentage = Column(Float, nullable=False)
    study_recommendation = Column(String, nullable=False)
    status = Column(String, default="to_study")  # 'to_study', 'studying', 'completed'
    questions_solved = Column(Integer, default=0)
    questions_correct = Column(Integer, default=0)

    edital = relationship("Edital", back_populates="topics")
    study_sessions = relationship("StudySession", back_populates="topic", cascade="all, delete-orphan")
