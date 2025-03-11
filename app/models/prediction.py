from pydantic import BaseModel, Field

class CustomerData(BaseModel):
    """Model for customer data input"""
    age: float
    time_spent_on_site: float
    pages_visited: int
    previous_purchases: int
    cart_value: float
    is_returning_customer: int = Field(..., ge=0, le=1)
    days_since_last_visit: float
    
class PredictionResponse(BaseModel):
    """Model for prediction response"""
    purchase_probability: float
    likely_to_purchase: bool