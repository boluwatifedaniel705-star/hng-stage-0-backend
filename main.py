from fastapi import FastAPI
from genderize import Genderize

app = FastAPI()

@app.get("/")
def home():
    return {"message":"API is running"}

@app.get("/api/classify")
def classify (name:str):

    #VALIDATION

    if name is None or name.strip() == "":
        return {"status":"Error", "message":"Name is required"}, 400
    
    if not isinstance (name, str):
        return {"status": "error", "message": "Name must be a string"}, 422

        