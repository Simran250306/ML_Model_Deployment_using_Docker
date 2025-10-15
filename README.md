Step 1: Install the Python requirements using command: pip install -r requiremenst.txt

Step 2: Install Docker and setup

Step 3: Open Docker and keep it running. Install Docker extension for Visual Studio Code

Step 4: To build Docker, run docker build -t image_name .

Step 5: To build Docker container, run  docker run --name container_name -p 8000:8000 image_name

Step 6: Uvicorn will start running on http://localhost:8000 and will show message {"message":"Iris model API"}

Step 7: Open Postman, select POST request and paste this link http://localhost:8000/predict 
        Select Body -> raw -> write {"features": [1, 2, 3, 4]} => class Virginica
        You can use different values in features from data.dict present in client.py or you custom values and predict classes