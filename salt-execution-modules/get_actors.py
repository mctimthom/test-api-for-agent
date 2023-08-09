# /srv/salt/_modules/get_actors.py
import requests

def get_actors():
    try:
        url = "http://localhost:5000/get_actors"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: Unable to fetch data from agnes's API. Status Code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error connecting to agnes's API: {e}")
        return None

