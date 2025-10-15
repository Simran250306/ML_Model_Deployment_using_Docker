# Theory and Design Notes for Iris Model Deployment

This document explains the theory, design decisions, and operational details for the Iris classification model and its Docker-based deployment found in this repository.

## High-level overview

- Problem: multiclass classification of Iris flower species (setosa, versicolor, virginica) from 4 numeric features: sepal length, sepal width, petal length, petal width.
- Model: scikit-learn RandomForestClassifier trained on the classic Iris dataset (included in scikit-learn).
- Serving: FastAPI application that loads a serialized model (joblib) and exposes a small HTTP API for predictions.
- Deployment: Docker image built from a lightweight Python base (official python:3.11 image). Uvicorn runs the FastAPI app on port 8000.

## Data and features

- Input features: an array/list with 4 numeric values in the order used by scikit-learn's Iris dataset: [sepal length, sepal width, petal length, petal width].
- Expected shape: a single sample is accepted as a 1D list and reshaped to (1, 4) before prediction.
- Validation: the current implementation does minimal validation — it assumes the client provides a list of 4 numeric values. Production systems should validate types, length, ranges and handle missing values explicitly.

## Model training and serialization

- Training script: `run.py` trains a RandomForestClassifier on the entire Iris dataset and writes the fitted model to `app/model.joblib` using joblib.dump.
- Why Random Forest: robust, performs well with little tuning and is tolerant of numeric features without heavy normalization (tree-based models are invariant to monotonic transforms). Good default for tabular classification.
- Serialization: joblib is recommended for scikit-learn models because it efficiently stores numpy arrays and Python objects. The model file `app/model.joblib` is loaded by the server at startup with `joblib.load('app/model.joblib')`.

Security note: the model file is a pickled artifact under the hood. Only load model files from trusted sources to avoid arbitrary code execution risks.

## Serving API

- Root endpoint (`GET /`) — a simple health/info endpoint returning {"message": "Iris model API"}.
- Prediction endpoint (`POST /predict`) — accepts JSON body `{"features": [f1, f2, f3, f4]}` and returns `{"predicted_class": "setosa"}`.
- Input handling: server converts the list to a numpy array and reshapes to (1, -1) before passing to `model.predict()`.
- Output mapping: numeric class labels (0,1,2) are mapped to readable names using a numpy array `class_names = ['setosa','versicolor','virginica']`.

Limitations and improvements:
- Currently, the server does not validate input shape or types and may raise server errors if a client provides malformed JSON or wrong-length lists. Add Pydantic models (FastAPI) to validate inputs and provide clear HTTP 4xx responses.
- Consider supporting batch predictions (multiple samples) by accepting a 2D array and returning an array of classes.
- Add content-type checks and require `application/json` for prediction requests.

## Docker deployment

- The `Dockerfile` uses `python:3.11` as the base image, copies `requirements.txt`, installs dependencies, copies the `app/` directory and exposes port 8000.
- The container command runs Uvicorn: `uvicorn app.server:app --host 0.0.0.0 --port 8000`. This is sufficient for development and simple deployments.

Production considerations:
- Use a process manager or run multiple workers behind a reverse proxy for production traffic (e.g., Gunicorn with Uvicorn workers or Kubernetes + Horizontal Pod Autoscaling).
- Pin dependency versions in `requirements.txt` to avoid unexpected changes. Consider using a lockfile for reproducible builds (pip-tools, poetry, or pip freeze).
- Keep model file size and memory usage in mind. Optimize model if necessary (prune trees, use lighter models) or use model quantization/compilation for performance-critical scenarios.

## How to run locally (dev)

1. Create a virtual environment and install dependencies:

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt

2. Train and save the model (creates `app/model.joblib`):

   python run.py

3. Run the FastAPI server with Uvicorn:

   uvicorn app.server:app --reload --host 0.0.0.0 --port 8000

4. Send a prediction request (examples):

   - Using `client.py` (provided): run `python client.py` after starting the server.
   - Using curl (PowerShell):

     curl -Method POST -ContentType 'application/json' -Body '{"features": [5.1, 3.5, 1.4, 0.2]}' http://localhost:8000/predict

## How to build and run with Docker

1. Build the image:

   docker build -t iris-model:latest .

2. Run the container:

   docker run --name iris-container -p 8000:8000 iris-model:latest

3. Test the service at `http://localhost:8000` or post to `/predict` as above.

## Error modes and edge cases

- Invalid JSON: FastAPI will return a 422 response by default for invalid body parsing. Improve error messages with Pydantic models.
- Wrong feature length/type: the server will raise an exception when reshaping/when model.predict encounters invalid input. Add explicit checks and return 400 Bad Request with helpful messages.
- Missing model file: the container will fail at startup if `app/model.joblib` is not present. Ensure `run.py` is run before building the image or add build-time steps to train or include a pre-trained model.

## Testing & validation

- Unit tests: add tests for the API endpoints (pytest + TestClient from FastAPI) and for data validation logic.
- Integration tests: start the app in a test container and run a small suite that posts sample inputs and checks outputs.

## Next steps and optional improvements

1. Add Pydantic request/response schemas to `app/server.py` for input validation and automatic OpenAPI documentation.
2. Add logging, structured tracing (OpenTelemetry), and metrics (Prometheus) to monitor predictions and model behavior.
3. Add CI to automatically run linters, tests, and build a Docker image on changes.
4. Add model versioning and a simple model registry or S3 storage for larger models.
5. Harden Docker image (non-root user, smaller base image like python:3.11-slim, multi-stage builds) and set explicit WORKDIR ownership.

## Short checklist for packaging a release

- Ensure `app/model.joblib` exists and is the desired model version.
- Pin dependencies and produce a lockfile.
- Verify the Docker image runs with a non-root user and exposes correct ports.
- Add health/readiness endpoints for orchestration platforms.

---

If you want, I can also: (a) add Pydantic models and improve input validation in `app/server.py`, (b) add unit tests for the API, or (c) create a minimal CI workflow and updated `requirements.txt` with pinned versions.
