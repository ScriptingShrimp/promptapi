import requests

def get_current_weather(city: str) -> Dict[str, Any]:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_API_KEY"
    response = requests.get(url)
    json_data = response.json()
    return json_data