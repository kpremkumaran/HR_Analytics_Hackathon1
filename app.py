
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# 1. Define Input Schema (Use 'str' instead of 'object')
class Input(BaseModel):
    city: str
    city_development_index: float
    gender: str
    relevent_experience: str
    enrolled_university: str
    education_level: str
    major_discipline: str  
    experience: str
    company_size: str
    company_type: str
    last_new_job: str
    training_hours: float

class Output(BaseModel):
    target: int

# 2. Load model ONCE globally for speed
model = joblib.load('jobchg_pipeline_model.pkl')

@app.get("/")
def read_root():
    return {"status": "API is online", "model": "HR Analytics Predictor"}

@app.post("/predict", response_model=Output)
def pr(payload: Input):
    # 3. Convert incoming data to DataFrame
    # Use payload.dict() to get the actual data sent in the request
    X_input = pd.DataFrame([payload.dict()])
    
    # 4. Predict
    prediction = model.predict(X_input)
    
    # 5. Return the result as the Output class
    return Output(target=int(prediction[0]))
