"""lecture 12: Pydantic request/response models."""
from typing import List
from pydantic import BaseModel, Field

class WeatherResponse(BaseModel):
    city: str
    temperature_c: float = Field(..., description="ტემპერატურა °C-ში")
    wind_speed_kmh: float

class CurrencyRate(BaseModel):
    code: str
    name: str
    quantity: int
    rate: float

class CurrencyResponse(BaseModel):
    date: str
    rates: List[CurrencyRate]

class SeismicEvent(BaseModel):
    event_id: str
    magnitude: float
    place: str
    latitude: float
    longitude: float
    depth_km: float

class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"
