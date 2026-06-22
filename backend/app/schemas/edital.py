from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class TopicAnalysis(BaseModel):
    name: str
    weight: str
    relevance_percentage: float
    study_recommendation: str

class MetadataAnalysis(BaseModel):
    extracted_topics_count: int
    status: Optional[str] = "Sucesso"

class AnalysisResponse(BaseModel):
    metadata: MetadataAnalysis
    topics: List[TopicAnalysis]
    general_strategy: str
