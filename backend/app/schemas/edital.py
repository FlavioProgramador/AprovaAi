from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class TopicAnalysis(BaseModel):
    id: Optional[int] = None
    name: str
    weight: str
    relevance_percentage: float
    study_recommendation: str
    status: Optional[str] = "to_study"
    questions_solved: Optional[int] = 0
    questions_correct: Optional[int] = 0

    class Config:
        from_attributes = True

class MetadataAnalysis(BaseModel):
    edital_id: Optional[int] = None
    extracted_topics_count: int
    status: Optional[str] = "Sucesso"

class AnalysisResponse(BaseModel):
    metadata: MetadataAnalysis
    topics: List[TopicAnalysis]
    general_strategy: str

    class Config:
        from_attributes = True

class TopicUpdate(BaseModel):
    status: str  # 'to_study', 'studying', 'completed'
    questions_solved: int
    questions_correct: int

class SessionCreate(BaseModel):
    topic_id: int
    duration_minutes: int

class SessionResponse(BaseModel):
    id: int
    topic_id: int
    duration_minutes: int
    created_at: datetime

    class Config:
        from_attributes = True
