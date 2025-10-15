Quick start (Windows PowerShell)

1) Create and activate a virtual environment, then install requirements:

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt

2) Train the model and save it to `app/model.joblib`:

   python run.py

3) Run the FastAPI server (development):

   uvicorn app.server:app --reload --host 0.0.0.0 --port 8000

   Open http://localhost:8000/ to check the root endpoint (should return {"message": "Iris model API"}).

4) Frontend (two options):

   - Same-origin (recommended): open the page served by the API:

       http://localhost:8000/ui

     This avoids CORS/preflight issues.

   - Static server (alternate): serve the repo root and open the page at:

       python -m http.server 8001
       http://localhost:8001/frontend.html

     If using this option, ensure the API is running and that CORS is enabled (the app already includes permissive CORS for development).

5) Test prediction endpoints manually (PowerShell examples):

   # GET root
   curl http://localhost:8000/

   # POST predict (JSON body) using Postman 
   curl -Method POST -ContentType 'application/json' -Body '{"features": [5.1, 3.5, 1.4, 0.2]}' http://localhost:8000/predict

6) Docker

   Build image:

     docker build -t iris-model:latest .

   Run container (map port 8000):

     docker run --name iris-container -p 8000:8000 iris-model:latest

   Note: The Docker image expects `app/model.joblib` to be present in the `app/` directory at build time. Run `python run.py` locally before building, or modify the Dockerfile to include model training or download steps.

Troubleshooting

- CORS errors ("Failed to fetch" in browser):
  - Prefer serving the frontend from the same origin (`/ui`) to avoid CORS during development.
  - If you serve the page from a different origin (file:// or http://localhost:8001), ensure the server is running and that the OPTIONS preflight returns Access-Control-Allow-Origin. The app includes permissive CORS for development but a server restart may be required after edits.

- Model file missing: if you get a startup error about `app/model.joblib`, run `python run.py` to generate the model.

- If Uvicorn exits unexpectedly when testing from scripts, prefer starting it without `--reload` if you need a stable background process for automated scripts.

Step 1: Install the Python requirements using command: pip install -r requiremenst.txt

Step 2: Install Docker and setup

Step 3: Open Docker and keep it running. Install Docker extension for Visual Studio Code

Step 4: To build Docker, run docker build -t image_name .

Step 5: To build Docker container, run  docker run --name container_name -p 8000:8000 image_name

Step 6: Uvicorn will start running on http://localhost:8000 and will show message {"message":"Iris model API"}

Step 7: Open Postman, select POST request and paste this link http://localhost:8000/predict 
        Select Body -> raw -> write {"features": [1, 2, 3, 4]} => class Virginica
        You can use different values in features from data.dict present in client.py or you custom values and predict classes.