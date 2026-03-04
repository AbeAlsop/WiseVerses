import requests
import datetime

def get_celebrations(date):
    url = f"http://calapi.inadiutorium.cz/api/v0/en/calendars/default/{date.year}/{date.month}/{date.day}"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    return [celebration['title'] for celebration in response.json().get('celebrations',[])]

if __name__ == "__main__":
    print(get_celebrations(datetime.date(2020, 3, 4)))