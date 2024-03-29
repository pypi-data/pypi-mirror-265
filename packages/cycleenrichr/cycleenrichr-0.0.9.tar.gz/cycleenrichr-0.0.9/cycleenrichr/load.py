
import requests
import os

DATA_URL = "https://mssm-data.s3.amazonaws.com/px_predictions.2.1.2.h5"

def download(path):
    response = requests.get(DATA_URL)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully to {path}")
    else:
        print(f"Failed to download file, status code: {response.status_code}")


