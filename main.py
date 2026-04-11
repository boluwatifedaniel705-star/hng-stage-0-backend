from fastapi import FastAPI
from genderize import Genderize
from datetime import datetime, timezone

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running"}

@app.get("/api/classify")
def classify(name: str):

    # VALIDATION

    if name is None or name.strip() == "":
        return {"status": "error", "message": "Name is required"}, 400
    
    if not isinstance(name, str):
        return {"status": "error", "message": "Name must be a string"}, 422
    
    
        # CALL GENDERIZE API
    result = get_gender_data(name)

    if result is None:
        return {"status": "error", "message": "Failed to reach Genderize API"}, 502

    gender = result.get("gender")
    probability = result.get("probability")
    count = result.get("count")

    # EDGE CASE: gender missing or no data
    if gender is None or count == 0:
        return {
            "status": "error",
            "message": "No prediction available for the provided name"
        }

    # CONFIDENCE LOGIC
    is_confident = (probability >= 0.7 and count >= 100)

    # SUCCESS RESPONSE
    return {
        "status": "success",
        "data": {
            "name": name,
            "gender": gender,
            "probability": probability,
            "sample_size": count,
            "is_confident": is_confident,
            "processed_at": datetime.now(timezone.utc).isoformat()
        }
    }

def get_gender_data(name):
    try:
        return Genderize().get([name])[0]
    except Exception:
        return None
