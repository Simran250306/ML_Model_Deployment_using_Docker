from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import joblib
import numpy as np

model = joblib.load('app/model.joblib')

class_names = np.array(['setosa', 'versicolor', 'virginica'])

app = FastAPI()

# Enable CORS so a static frontend (served from file:// or another host) can call this API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the repository root (one level up from app/) as static so we can serve the frontend
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
try:
    app.mount('/static', StaticFiles(directory=project_root), name='static')
except Exception:
    # If mounting static fails in some environments, continue without crashing; serving will be best-effort
    pass


@app.get('/ui')
def ui():
    """Return the frontend HTML from the repository root so the page and API share origin (no CORS needed)."""
    frontend_path = os.path.join(project_root, 'frontend.html')
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path, media_type='text/html')
    return {'error': 'frontend not found'}

@app.get('/')
def read_root():
    return {'message': 'Iris model API'}

@app.post('/predict')
def predict(data: dict):
    """
    Predicts the class of a given set of features.

    Args:
        data (dict): A dictionary containing the features to predict.
        e.g. {"features": [1, 2, 3, 4]}

    Returns:
        dict: A dictionary containing the predicted class.
    """        
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)
    class_name = class_names[prediction][0]
    return {'predicted_class': class_name}
