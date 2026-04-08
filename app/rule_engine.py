from typing import List
from models import Load, Driver, MatchedDriver, ScoreBreakdown
from utils import haversine_distance
from config import WEIGHT_PROXIMITY, WEIGHT_RATING, WEIGHT_HISTORY

# Weights for our scoring logic
WEIGHTS = {
    "proximity_wt": WEIGHT_PROXIMITY,
    "rating_wt": WEIGHT_RATING,
    "history_wt": WEIGHT_HISTORY
}

def score_and_rank_drivers(load: Load, drivers: List[Driver], max_distance_km: int) -> List[MatchedDriver]:
    ranked_results = []
    
    for driver in drivers:
        # Distance calculation
        dist_km = haversine_distance(
            load.pickup_coordinates.lat, load.pickup_coordinates.lng,
            driver.current_coordinates.lat, driver.current_coordinates.lng
        )
        
        # Hard Filter at python logic level (If DB provides wider parameters, filter here)
        if dist_km > max_distance_km:
            continue
            
        # 1. Proximity Score (Max 40 points) -> closer is better
        prox_score_raw = max(0, max_distance_km - dist_km) / max_distance_km
        proximity_score = prox_score_raw * WEIGHTS["proximity_wt"]
        
        # 2. Rating Score (Max 30 points) -> rating out of 5 translates directly
        rating_score = (driver.rating / 5.0) * WEIGHTS["rating_wt"]
        
        # 3. History Score (Max 30 points) -> completion out of 100
        history_score = (driver.completion_rate / 100.0) * WEIGHTS["history_wt"]
        
        # Total
        total_match_score = proximity_score + rating_score + history_score 
        
        # Formatting breakdown
        breakdown = ScoreBreakdown(
            proximity_score=round(proximity_score, 2),
            rating_score=round(rating_score, 2),
            history_score=round(history_score, 2)
        )
        
        ranked_results.append(
            MatchedDriver(
                driver_id=driver.driver_id,
                distance_km=round(dist_km, 2),
                match_score=round(total_match_score, 2),
                breakdown=breakdown
            )
        )
        
    # Sort results highest score to lowest score
    ranked_results.sort(key=lambda x: x.match_score, reverse=True)
    return ranked_results
