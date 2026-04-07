from ml_engine import score_and_rank_drivers_ml
from dummy_db import MOCK_LOADS, MOCK_DRIVERS

print("Testing direct inference...")
res = score_and_rank_drivers_ml(MOCK_LOADS[0], MOCK_DRIVERS, 500)
for r in res:
    print(r.model_dump())
