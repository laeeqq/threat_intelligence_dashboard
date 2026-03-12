from flask import Flask, jsonify
import pandas as pd
import requests
import os # Importing the os module to access environment variables, which is essential for securely managing sensitive information like API keys.
import sqlite3
from dotenv import load_dotenv #required to load environment variables from a .env file, allowing you to keep sensitive information like API keys out of your codebase and manage them securely.

load_dotenv() # Load environment variables from .env file

app = Flask(__name__) #Create Flask app instance

API_KEY = os.getenv("ABUSEIPDB_KEY")

# Get the absolute path to the database file so Flask always finds it regardless of which process is running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "threats.db")

def init_db():
    conn = sqlite3.connect(DB_PATH) # Open connection using absolute path
    cursor = conn.cursor() # Create cursor object to execute SQL commands
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT NOT NULL,
            country_code TEXT,
            abuse_score INTEGER,
            last_reported TEXT,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """) # Create threats table if it doesnt already exist
   
    conn.commit() # Save changes permanently to the database file
    conn.close() # Close the connection to free up memory
    print("Database initialized at:", DB_PATH)

def save_threats(df):

    conn = sqlite3.connect(DB_PATH) # Open connection using absolute path
    cursor = conn.cursor() # Create cursor to execute SQL commands
    saved = 0 # Counter to track how many rows were saved
    
    
    for _, row in df.iterrows(): # Loop through every row in the DataFrame
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO threats
                (ip_address, country_code, abuse_score, last_reported)
                VALUES (?, ?, ?, ?)
            """, (
                row["ipAddress"], # IP address of the malicious host
                row["countryCode"], # Country the IP is from
                row["abuseConfidenceScore"], # How dangerous the IP is 0-100
                row["lastReportedAt"] # When the IP was last reported as malicious
            )) # INSERT OR IGNORE skips duplicates instead of crashing
            
            saved += 1 # Increment counter for each successful insert
        except Exception as e:
            print("Error saving row:", e) # Print any errors without crashing the whole loop
  
    conn.commit() # Save all inserts permanently in one go
    conn.close() # Close connection to free up memory
    print(f"Saved {saved} threats to database")
    
def get_stats():
    conn = sqlite3.connect(DB_PATH) # Open connection using absolute path
    
    df = pd.read_sql_query("SELECT * FROM threats", conn) # Load all threat data into a DataFrame

    conn.close()

    if df.empty:
        return {"error: NO data in database yet"}
    
    stats = {
        "total_threats": len(df), # Total number of threats in the database
        "top_countries": df["country_code"].value_counts().head(10).# Top 10 countries with the most threats
    }

def fetch_blacklist():
   
    url = "https://api.abuseipdb.com/api/v2/blacklist" # AbuseIPDB endpoint for fetching the blacklist
    headers = {
        "Key": API_KEY, # API key for authentication
        "Accept": "application/json" # Tell AbuseIPDB we want JSON back
    }
    
    params = {"limit": 100} # Only fetch 100 IPs to stay within free tier limits
    response = requests.get(url, headers=headers, params=params) # Make the HTTP GET request
    data = response.json() # Parse the response as JSON into a Python dictionary
    
    if "data" not in data:
        return None, data # If something went wrong return the error info
    df = pd.DataFrame(data["data"]) # Convert the list of IPs into a pandas DataFrame
    return df, None # Return the DataFrame and no error

@app.route("/") # Route for the home page
def home():
    return "Threat Dashboard is live!"

@app.route("/api/threats") # Route that returns threat data as JSON

def threats():
    df, error = fetch_blacklist() # Fetch live threat data from AbuseIPDB
    if error:
        return jsonify({"error": error}), 400 # Return error as JSON with 400 status code
    save_threats(df) # Save the fetched threat data to the SQLite database
    return jsonify(df.to_dict(orient="records")) # Convert DataFrame to JSON and return it

if __name__ == "__main__":
    init_db() # Initialize the database when the application starts
    app.run(debug=True)
