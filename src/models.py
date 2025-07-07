from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class Confidence(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class HazmatClassification(BaseModel):
    product_id: str = Field(..., description="The unique identifier of the product.")
    is_hazmat: bool = Field(..., description="Indicates whether the product is classified as a Hazmat.")
    reason: Optional[str] = Field(None, description="The reason for the classification, if the product is a Hazmat.")
    confidence: Optional[Confidence] = Field(None, description="The confidence level of the classification, if the product is a Hazmat.")

