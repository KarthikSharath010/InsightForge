from pydantic import BaseModel, Field
from typing import List

class StrategicGap(BaseModel):
    title: str = Field(description="The core competitive weakness identified")
    evidence: str = Field(description="Direct fact or quote from the PDF")
    recommendation: str = Field(description="Actionable strategy to beat the competitor")

class IntelligenceState(BaseModel):
    competitor_name: str
    gaps: List[StrategicGap]
    dialogue_script: str