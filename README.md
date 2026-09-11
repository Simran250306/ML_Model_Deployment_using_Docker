# Iris Model Deployment with Docker

This project demonstrates how to train a small machine-learning model and serve it as a web application inside Docker.

The project uses the built-in scikit-learn Iris dataset. A Random Forest classifier learns to identify an iris flower as `setosa`, `versicolor`, or `virginica` from four measurements:

- Sepal length
- Sepal width
- Petal length
- Petal width

The trained model is exposed through a FastAPI API, and a browser-based frontend lets users enter measurements and request predictions.

## How It Works

1. `run.py` loads the Iris dataset and trains a `RandomForestClassifier`.
2. The trained model is saved to `app/model.joblib`.
3. `app/server.py` loads the saved model when the API starts.
4. `POST /predict` receives flower measurements and returns the predicted species.
5. `GET /ui` serves the browser frontend.
6. The `Dockerfile` packages the API, model, frontend, and Python dependencies into one image.

## Project Structure

```text
.
├── app/
│   ├── model.joblib       # Saved trained model
│   └── server.py          # FastAPI application
├── client.py              # Example script for sending predictions
├── Dockerfile             # Docker image definition
├── frontend.html          # Browser interface
├── requirements.txt       # Python dependencies
└── run.py                 # Model training script
```

## Requirements

- Python 3.11 or compatible Python 3 version
- Docker Desktop, if running the container

## Run Locally Without Docker

From the project directory in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
uvicorn app.server:app --reload --host 0.0.0.0 --port 8000
```

Open the frontend at:

```text
http://localhost:8000/ui
```

## Run with Docker

Generate the model before building the image:

```powershell
python run.py
```

Build the image:

```powershell
docker build -t iris-model:latest .
```

Start a container:

```powershell
docker run --name iris-container -p 8000:8000 iris-model:latest
```

The application is now available at:

```text
http://localhost:8000/ui
```

To stop and remove the container later:

```powershell
docker rm -f iris-container
```

## Use from Another Device

The Docker port mapping publishes port `8000` on the host computer. To access the application from a phone or another computer on the same Wi-Fi network:

1. Find the host computer's local IPv4 address:

   ```powershell
   ipconfig
   ```

2. Find the address for the active network adapter, such as `192.168.1.42`.
3. Open this URL on the other device:

   ```text
   http://192.168.1.42:8000/ui
   ```

Use the host computer's IP address instead of `localhost`. If Windows Firewall blocks the connection, allow inbound TCP traffic on port `8000` for private networks.

This setup provides local-network access only. It does not publish the application to the public internet.

## API Endpoints

### Health check

```http
GET /
```

Response:

```json
{"message":"Iris model API"}
```

### Prediction

```http
POST /predict
Content-Type: application/json
```

Request:

```json
{"features":[5.1,3.5,1.4,0.2]}
```

Response:

```json
{"predicted_class":"setosa"}
```

PowerShell example:

```powershell
Invoke-RestMethod -Uri http://localhost:8000/predict `
  -Method Post `
  -ContentType 'application/json' `
  -Body '{"features":[5.1,3.5,1.4,0.2]}'
```

## Notes

- The model file must exist at `app/model.joblib` before building the Docker image.
- The frontend uses the same-origin `/predict` URL, so it works through `localhost` and through the host computer's network IP.
- The permissive CORS configuration is intended for development and demonstration purposes.