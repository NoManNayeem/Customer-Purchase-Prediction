import joblib
import pandas as pd
from app.models.prediction import CustomerData, PredictionResponse

class PredictorService:
    """Service for making predictions with the model"""
    
    def __init__(self, model_path: str):
        """Initialize with model path"""
        self.model = joblib.load(model_path)
        
    def predict(self, data: CustomerData) -> PredictionResponse:
        """Make prediction for a single customer"""
        # Convert to DataFrame for prediction
        df = pd.DataFrame([data.dict()])
        
        # Add engineered features (same as in training)
        df['recency_score'] = 1 / (1 + df['days_since_last_visit'])
        df['engagement_score'] = (df['time_spent_on_site'] * df['pages_visited']) / 10
        
        # Make prediction
        probability = self.model.predict_proba(df)[0][1]
        is_likely = probability >= 0.5
        
        return PredictionResponse(
            purchase_probability=float(probability),
            likely_to_purchase=bool(is_likely)
        )