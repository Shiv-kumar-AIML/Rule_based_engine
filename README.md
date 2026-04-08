# AI Dispatch Engine: Rule-Based & ML-Powered Matching

A fleet dispatch matching service that connects loads with the most suitable drivers using a hybrid rule-based and machine-learning approach. Built with **FastAPI** and **LightGBM**, this system provides a flexible framework for real-time dispatch scoring and ranking.

---

## 🚀 Overview

This project implements a multi-phase dispatch engine designed to optimize the matching process between available drivers and load requirements. It supports:

- **Phase 1: Rule-Based Scoring** – A deterministic score based on proximity, driver rating, and historical completion rates.
- **Phase 3: machine Learning Inference** – Predictive matching using a trained LightGBM model to estimate the probability of match acceptance.

## 🛠️ Tech Stack

- **API**: FastAPI (Python)
- **Data Handling**: Pandas, Pydantic
- **ML Engine**: LightGBM, Scikit-learn
- **Environment**: Python 3.9+
- **Mock DB**: In-memory data structures for rapid prototyping and testing.

---

## 📂 Project Structure

```text
├── app/
│   ├── main.py            # FastAPI Entrypoint & Endpoints
│   ├── rule_engine.py      # Rule-based scoring logic
│   ├── ml_engine.py        # ML inference logic (LightGBM)
│   ├── models.py           # Pydantic Data Models
│   ├── dummy_db.py         # Mock data & access layers
│   ├── config.py           # Application configuration
│   └── utils.py            # Shared utility functions (e.g., Haversine)
├── Model_training/
│   ├── train.ipynb         # End-to-end ML training pipeline
│   └── Model/              # Directory for trained model artifacts
├── pyproject.toml          # Project dependencies
└── .env                    # Environment configuration
```

---

## ⚙️ Setup & Installation

1. **Clone the repository**
2. **Install Dependencies**:

   ```bash
   pip install fastapi uvicorn pandas scikit-learn lightgbm jupyter python-dotenv
   ```

   *(Or use `uv sync` if following the project's preferred lockfile)*
3. **Configure Environment**:
   Create a `.env` file in the root directory (refer to `config.py` for variables).
4. **Run the Server**:

   ```bash
   uvicorn app.main:app --reload
   ```

---

## 📡 API Documentation

### **Match Drivers for Load**

`POST /api/v1/dispatch/match`

Finds and ranks eligible drivers for a specific load.

**Request Body:**

```json
{
  "load_id": "L-001",
  "max_distance_km": 100,
  "use_ml": false
}
```

**Response Body:**

```json
{
  "load_id": "L-001",
  "total_eligible_drivers_found": 2,
  "matches": [
    {
      "driver_id": "D-789",
      "distance_km": 15.4,
      "match_score": 85.5,
      "breakdown": {
        "proximity_score": 35.0,
        "rating_score": 25.5,
        "history_score": 25.0
      }
    }
  ]
}
```

---

## 🧠 ML Pipeline

The `Model_training/train.ipynb` notebook provides a complete workflow for:

1. Data Engineering & Feature Extraction.
2. Model Training using LightGBM.
3. Evaluation & Artifact Generation (Pickle).

The generated models are used by `app/ml_engine.py` when the `use_ml` flag is set to `true` in the API request.

---

## 🧪 Testing

To test the matching logic directly without running the FastAPI server:

```bash
python app/test_inference.py
```
