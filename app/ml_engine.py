import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
os.environ['OMP_NUM_THREADS']='1'
import pickle
import pandas as pd
from typing import List
from models import Load, Driver, MatchedDriver, ScoreBreakdown
from utils import haversine_distance
from config import ML_MODEL_DIR, MODEL_XGB_FILE, MODEL_FEATURES_FILE, WEIGHT_PROXIMITY, WEIGHT_RATING, WEIGHT_HISTORY
import logging

logger = logging.getLogger(__name__)

# Paths for the generated model files
MODEL_PATH = os.path.join(ML_MODEL_DIR, MODEL_XGB_FILE)
FEATURES_PATH = os.path.join(ML_MODEL_DIR, MODEL_FEATURES_FILE)

# Load Global Model into memory if exists
try:
    with open(MODEL_PATH, "rb") as f:
        xgb_model = pickle.load(f)
    with open(FEATURES_PATH, "rb") as f:
        feature_names = pickle.load(f)
    logger.info("✅ ML Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load ML Model: {e}")
    xgb_model = None
    feature_names = None

def score_and_rank_drivers_ml(load: Load, drivers: List[Driver], max_distance_km: int) -> List[MatchedDriver]:
    if not xgb_model or not feature_names:
        logger.warning("Models not loaded. Returning empty ML results.")
        return []

    ranked_results = []
    
    # Pre-parse categorical OHE
    req_truck = load.required_truck_type.lower()
    is_dry_van = 1 if "dry" in req_truck else 0
    is_flatbed = 1 if "flatbed" in req_truck else 0
    is_reefer = 1 if "reefer" in req_truck else 0

    for driver in drivers:
        # 1. Distance Calculation (Deadhead)
        deadhead_dist_km = haversine_distance(
            load.pickup_coordinates.lat, load.pickup_coordinates.lng,
            driver.current_coordinates.lat, driver.current_coordinates.lng
        )
        
        # Hard Filter
        if deadhead_dist_km > max_distance_km:
            continue
            
        # Calculate trip distance from pickup to drop
        trip_distance_km = haversine_distance(
            load.pickup_coordinates.lat, load.pickup_coordinates.lng,
            load.drop_coordinates.lat, load.drop_coordinates.lng
        )
        if trip_distance_km == 0:
            trip_distance_km = 1.0 # Avoid division by zero
            
        rating = driver.rating
        # Depending on how it's represented (45 vs 0.45)
        comp_rate = driver.completion_rate / 100.0 if driver.completion_rate > 1.0 else driver.completion_rate
        
        # Build feature dict
        feats = {
            "driver_rating": rating,
            "completion_rate": comp_rate,
            "acceptance_rate": driver.acceptance_rate,
            "total_jobs": driver.total_jobs,
            "load_weight": load.weight,
            "distance_km": trip_distance_km,
            "urgency": load.urgency,
            "driver_to_pickup_distance": deadhead_dist_km,
            "past_route_success": driver.past_route_success,
            "bid_price": driver.bid_price,
            "price_deviation": driver.price_deviation,
            "response_time": driver.response_time,
            "driver_score": driver.driver_score,
            "price_per_km": driver.bid_price / trip_distance_km,
            "load_type_dry_van": is_dry_van,
            "load_type_flatbed": is_flatbed,
            "load_type_reefer": is_reefer
        }
        
        # 3. Create DataFrame obeying feature_names order
        df_feats = pd.DataFrame([feats], columns=feature_names)
        
        # Predict target 1 (Acceptance Probability)
        probability = float(xgb_model.predict_proba(df_feats)[0][1])
        
        # Pure ML score ranking, no rules overlap
        ml_score = probability * 100
        
        ranked_results.append(
            MatchedDriver(
                driver_id=driver.driver_id,
                distance_km=round(deadhead_dist_km, 2),
                match_score=round(ml_score, 2),
                ml_probability=round(probability, 4),
                breakdown=None
            )
        )
        
    # Sort highest ML prob to lowest
    ranked_results.sort(key=lambda x: x.match_score, reverse=True)
    return ranked_results
