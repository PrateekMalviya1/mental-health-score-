import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
import pandas as pd

model = joblib.load('Mental_Health_Score_Predictor.pkl')
app = FastAPI()

top_countries = ['Other', 'India', 'USA', 'Canada', 'UK', 'Australia', 'Germany', 'France', 'Maxico', 'Turkey']


class RequestDataSchema(BaseModel):
    # Define the structure of your input data here
    Age: int = Field(..., ge=10, le=100)
    Gender: Literal["Male", "Female"]
    Country: str
    Academic_Level: Literal["High School", "Undergraduate", "Graduate"]
    Most_Used_Platform: Literal["Facebook", "LinkedIn", "Instagram", "Snapchat", "Twitter", "YouTube", "TikTok", "LINE", "KakaoTalk", "VKontakte", 'WhatsApp', 'WeChat']
    Purpose_Of_Use: Literal["Networking", "Entertainment", "Education", "News"]
    Avg_Daily_Usage_Hours: float = Field(..., ge=0, le=24)
    Daily_Unlocks: int = Field(..., ge=0)
    Study_Hours: float = Field(..., ge=0, le=24)
    Physical_Activity_Hours: float = Field(..., ge=0, le=24)
    Sleep_Hours_Per_Night: float = Field(..., ge=0, le=24)
    Stress_Level: Literal["Low", "Medium", "High", "Very High"]  
    
    
class ResponseDataSchema(BaseModel):
    predicted_mental_health_score: float

@app.get("/")
def home():
    return {"message": "Welcome to the Mental Health Score Predictor API"}


@app.post("/predict", response_model=ResponseDataSchema)
def predict(data: RequestDataSchema):
    country_grouped = data.Country if data.Country in top_countries else 'Other'
    input_data = pd.DataFrame([{
        "Age": data.Age,
        "Gender": data.Gender,
        "Country": data.Country,
        "Academic_Level": data.Academic_Level,
        "Most_Used_Platform": data.Most_Used_Platform,
        "Purpose_Of_Use": data.Purpose_Of_Use,
        "Avg_Daily_Usage_Hours": data.Avg_Daily_Usage_Hours,
        "Daily_Unlocks": data.Daily_Unlocks,
        "Study_Hours": data.Study_Hours,
        "Physical_Activity_Hours": data.Physical_Activity_Hours,
        "Sleep_Hours_Per_Night": data.Sleep_Hours_Per_Night,
        "Stress_Level": data.Stress_Level,
        "grouped_countries": country_grouped
    }])
    
    pridiction = model.predict(input_data)[0]
    return ResponseDataSchema(predicted_mental_health_score=round(float(pridiction),2))


# ['Age',
#  'Gender',
#  'Country',
#  'Academic_Level',
#  'Most_Used_Platform',
#  'Purpose_Of_Use',
#  'Avg_Daily_Usage_Hours',
#  'Daily_Unlocks',
#  'Study_Hours',
#  'Physical_Activity_Hours',
#  'Sleep_Hours_Per_Night',
#  'Stress_Level',
#  'Mental_Health_Score']