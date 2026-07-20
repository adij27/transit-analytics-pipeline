from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    station_id: str = Field(..., example="72")
    month: int = Field(..., ge=1, le=12, example=7)
    day: int = Field(..., ge=1, le=31, example=15)
    day_of_week: int = Field(..., ge=1, le=7, example=3, description="1=Sunday, 7=Saturday")
    hour: int = Field(..., ge=0, le=23, example=8)
    is_weekend: int = Field(..., ge=0, le=1, example=0)


class PredictionResponse(BaseModel):
    station_id: str
    predicted_trips: float
    model_version: str
