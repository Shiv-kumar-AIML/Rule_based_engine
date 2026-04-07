import logging
from typing import Optional, List
from models import Load, Driver, Coordinates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- TEMPORARY MOCKED DATA ---
# Yeh real database ki jagah use ho raha hai for testing purposes
MOCK_LOADS = [
    Load(
        load_id="L-12345",
        pickup_coordinates=Coordinates(lat=28.7041, lng=77.1025), # Example: Delhi Coordinates
        drop_coordinates=Coordinates(lat=19.0760, lng=72.8777),   # Example: Mumbai Coordinates
        weight=15.0,
        urgency=2,
        required_truck_type="Flatbed",
        status="active"
    )
]

MOCK_DRIVERS = [
    Driver(
        driver_id="D-001",
        current_coordinates=Coordinates(lat=28.7100, lng=77.1100), # Delhi - Very close
        truck_type="Flatbed",
        rating=4.8,
        completion_rate=95.0,
        acceptance_rate=0.85,
        total_jobs=120,
        past_route_success=0.90,
        response_time=45.0,
        driver_score=0.45,
        bid_price=8500.0,
        price_deviation=0.05,
        status="available"
    ),
    Driver(
        driver_id="D-002",
        current_coordinates=Coordinates(lat=28.8000, lng=77.2000), # Farther away but valid
        truck_type="Flatbed",
        rating=4.0,
        completion_rate=80.0,
        acceptance_rate=0.60,
        total_jobs=45,
        past_route_success=0.40,
        response_time=130.0,
        driver_score=0.25,
        bid_price=7000.0,
        price_deviation=-0.10,
        status="available"
    ),
    Driver(
        driver_id="D-003",
        current_coordinates=Coordinates(lat=28.7200, lng=77.1200), # Driver with wrong truck
        truck_type="Reefer",
        rating=4.9,
        completion_rate=98.0,
        acceptance_rate=0.95,
        total_jobs=200,
        past_route_success=0.95,
        response_time=20.0,
        driver_score=0.50,
        bid_price=9500.0,
        price_deviation=0.20,
        status="available"
    ),
    Driver(
        driver_id="D-004",
        current_coordinates=Coordinates(lat=19.0760, lng=72.8777), # Mumbai - Too far
        truck_type="Flatbed",
        rating=4.5,
        completion_rate=90.0,
        acceptance_rate=0.75,
        total_jobs=85,
        past_route_success=0.65,
        response_time=90.0,
        driver_score=0.35,
        bid_price=8000.0,
        price_deviation=0.00,
        status="available"
    )
]

def get_load_by_id(load_id: str) -> Optional[Load]:
    """
    TEMP API: Fetch load details from dummy DB.
    TODO: Isko ek actual PostgreSQL + SQLAlchemy function me replace karna hai (e.g. session.query(Load).filter_by(...))
    """
    logger.info(f"Mock DB: Fetching load details for {load_id}")
    for load in MOCK_LOADS:
        if load.load_id == load_id:
            return load
    return None

def fetch_eligible_drivers(required_truck_type: str) -> List[Driver]:
    """
    TEMP API: Fetch active drivers with exact required truck type.
    TODO: Isko PostGIS SQL Query me replace karna hai jisme (ST_DWithin) ka upyog hoga or sirf active drivers ayenge.
    """
    logger.info(f"Mock DB: Fetching available drivers for truck type '{required_truck_type}'")
    valid_drivers = []
    for d in MOCK_DRIVERS:
        if d.status == "available" and d.truck_type == required_truck_type:
            valid_drivers.append(d)
    return valid_drivers
