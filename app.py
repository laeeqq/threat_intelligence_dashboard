from flask import Flask, jsonify
import pandas as pd
import requests
import os # Importing the os module to access environment variables, which is essential for securely managing sensitive information like API keys.
import sqlite3
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

app = Flask(__name__) #Create Flask app instance

API_KEY = os.getenv("ABUSEIPDB_KEY")

def fetch_blacklist():
    url = "https://api.abuseipdb.com/api/v2/blacklist" #Stores the API endpoint URL for fetching the blacklist data from AbuseIPDB.
    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }
    params = {"limit": 100}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if "data" not in data:
        return None, data  # return error info

    df = pd.DataFrame(data["data"])
    return df, None

@app.route("/")
def home():
    return "Threat Dashboard is live!"

@app.route("/api/threats")
def threats():
    df, error = fetch_blacklist()
    if error:
        return jsonify({"error": error}), 400
    return jsonify(df.to_dict(orient="records"))  #Convert the DataFrame to a list of dictionaries (records) and return it as JSON response.

if __name__ == "__main__":
    app.run(debug=True)