import os
import requests
import datetime
from dotenv import load_dotenv
load_dotenv()

#Alternative source: National Weather service
    #get NWS station for latitude/longitude
    #https://api.weather.gov/points/43.615,-116.702
    #Follow the "forecast" link in the results
    #https://api.weather.gov/gridpoints/BOI/133,86/forecast

def query_wolfram(query):
    app_id = os.getenv("WOLFRAM_API_KEY")
    return requests.get("https://api.wolframalpha.com/v1/result", params={"i": query, "appid": app_id})

def get_weather(location, day):
    response = query_wolfram(f"What was the weather on {day:%b %d, %Y} in {location}")
    return response.text if response.status_code == 200 else "No weather results"

if __name__ == "__main__":
    print(get_weather("Boise, ID", datetime.date(2026, 2, 24)))
    #print(query_wolfram("Where is Boise, Idaho?").text)