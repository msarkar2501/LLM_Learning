import requests

def get_coordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    response = requests.get(url)
    data = response.json()

    if "results" not in data:
        return None, None

    lat = data["results"][0]["latitude"]
    lon = data["results"][0]["longitude"]
    return lat, lon

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    data = response.json()

    weather = data["current_weather"]
    return f"Temperature: {weather['temperature']}°C, Wind: {weather['windspeed']} km/h, Code: {weather['weathercode']}"

# test them together
lat, lon = get_coordinates("Mumbai")
print(get_weather(lat, lon))