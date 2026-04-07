from fastapi import FastAPI, HTTPException
from models import MatchRequest, MatchResponse
import dummy_db
from rule_engine import score_and_rank_drivers
from ml_engine import score_and_rank_drivers_ml
from config import APP_NAME

app = FastAPI(title=APP_NAME)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Rule-Based Engine mock server is running"}

@app.post("/api/v1/dispatch/match", response_model=MatchResponse)
async def match_drivers_for_load(request: MatchRequest):
    """
    Core Dispatch Matching Endpoint.
    This accepts a load_id and searches valid drivers from database.
    """
    
    # 1. Fetch Load Constraints (TEMP CALL MOCKED)
    # TODO NEXT PHASE: Replace `get_load_by_id` with `SQLAlchemy query.get(Load, load_id)`
    load = dummy_db.get_load_by_id(request.load_id)
    if not load:
        raise HTTPException(status_code=404, detail="Load not found in database")
        
    # 2. Fetch Potential Drivers Match (TEMP CALL MOCKED)
    # TODO NEXT PHASE: Replace with `PostGIS` spatial queries inside PostgreSQL over drivers table
    eligible_drivers = dummy_db.fetch_eligible_drivers(load.required_truck_type)
    
    # 3. Apply Scoring Rule Engine or ML Engine
    if request.use_ml:
        matches = score_and_rank_drivers_ml(load, eligible_drivers, request.max_distance_km)
    else:
        matches = score_and_rank_drivers(load, eligible_drivers, request.max_distance_km)
    
    # 4. Formulate the valid response expected by Node.js
    return MatchResponse(
        load_id=load.load_id,
        total_eligible_drivers_found=len(matches),
        matches=matches
    )
