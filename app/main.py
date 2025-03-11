import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.models.prediction import CustomerData, PredictionResponse
from app.services.predictor import PredictorService

# Get the directory of this file (app directory)
app_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize FastAPI app
app = FastAPI(title="Purchase Prediction API")

# Mount static files directory (using absolute path)
static_dir = os.path.join(app_dir, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Set up templates directory (using absolute path)
templates_dir = os.path.join(app_dir, "templates")
templates = Jinja2Templates(directory=templates_dir)

# Construct the absolute path for the model file
# Assumes your project structure is:
#   Project_Root/
#     app/
#       main.py
#     downloaded_model/
base_dir = os.path.dirname(app_dir)
model_path = os.path.join(base_dir, "downloaded_model", "purchase_prediction_model.pkl")

# Initialize predictor service with the absolute model path
predictor_service = PredictorService(model_path)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Home page"""
    return templates.TemplateResponse("base.html", {"request": request})

@app.post("/predict")
async def predict(data: CustomerData):
    """API endpoint for prediction"""
    return predictor_service.predict(data)

@app.get("/predict-view", response_class=HTMLResponse)
async def predict_form(request: Request):
    """Web form for prediction"""
    return templates.TemplateResponse("prediction_form.html", {"request": request})

@app.post("/predict-view", response_class=HTMLResponse)
async def predict_form_submit(
    request: Request,
    age: float = Form(...),
    time_spent_on_site: float = Form(...),
    pages_visited: int = Form(...),
    previous_purchases: int = Form(...),
    cart_value: float = Form(...),
    is_returning_customer: int = Form(...),
    days_since_last_visit: float = Form(...)
):
    """Handle form submission and display result"""
    # Create CustomerData from form inputs
    data = CustomerData(
        age=age,
        time_spent_on_site=time_spent_on_site,
        pages_visited=pages_visited,
        previous_purchases=previous_purchases,
        cart_value=cart_value,
        is_returning_customer=is_returning_customer,
        days_since_last_visit=days_since_last_visit
    )
    
    # Make prediction
    result = predictor_service.predict(data)
    
    # Return form with result
    return templates.TemplateResponse(
        "prediction_form.html",
        {
            "request": request, 
            "result": result,
            "form_data": data.dict()
        }
    )
