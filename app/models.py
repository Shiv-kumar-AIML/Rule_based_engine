from pydantic import BaseModel
from typing import List

class Coordinates(BaseModel):
    lat: float
    lng: float

class Load(BaseModel):
    load_id: str
    pickup_coordinates: Coordinates
    drop_coordinates: Coordinates
    weight: float
    urgency: int
    required_truck_type: str
    status: str

class Driver(BaseModel):
    driver_id: str
    current_coordinates: Coordinates
    truck_type: str
    rating: float
    completion_rate: float
    acceptance_rate: float
    total_jobs: int
    past_route_success: float
    response_time: float
    driver_score: float
    bid_price: float
    price_deviation: float
    status: str

from config import DEFAULT_MAX_DISTANCE_KM

class MatchRequest(BaseModel):
    load_id: str
    max_distance_km: int = DEFAULT_MAX_DISTANCE_KM
    use_ml: bool = False

class ScoreBreakdown(BaseModel):
    proximity_score: float
    rating_score: float
    history_score: float

class MatchedDriver(BaseModel):
    driver_id: str
    distance_km: float
    match_score: float
    ml_probability: float | None = None
    breakdown: ScoreBreakdown | None = None

class MatchResponse(BaseModel):
    load_id: str
    total_eligible_drivers_found: int
    matches: List[MatchedDriver]
