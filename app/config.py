import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from the parent directory (project root)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# App Settings
APP_NAME = os.getenv("APP_NAME", "AI Dispatch Engine")
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")

# ML Engine Paths
ML_MODEL_DIR = os.getenv("ML_MODEL_DIR", "")
MODEL_XGB_FILE = os.getenv("MODEL_XGB_FILE", "xgb_model.pkl")
MODEL_FEATURES_FILE = os.getenv("MODEL_FEATURES_FILE", "feature_names.pkl")

# Rule Engine Weights
WEIGHT_PROXIMITY = float(os.getenv("WEIGHT_PROXIMITY", "40.0"))
WEIGHT_RATING = float(os.getenv("WEIGHT_RATING", "30.0"))
WEIGHT_HISTORY = float(os.getenv("WEIGHT_HISTORY", "30.0"))

# Dispatch Logic
DEFAULT_MAX_DISTANCE_KM = int(os.getenv("DEFAULT_MAX_DISTANCE_KM", "50"))
