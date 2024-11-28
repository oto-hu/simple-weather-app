import requests
import os
from datetime import datetime

class WeatherApp:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
        self.base_url = 'http://api.openweathermap.org/data/2.5/weather'

    def get_weather(self, city):
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            weather_info = {
                'city': data['name'],
                'temperature': round(data['main']['temp']),
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            return weather_info

        except requests.exceptions.RequestException as e:
            return {'error': f'Error fetching weather data: {str(e)}'}

def main():
    # APIキーを環境変数から取得
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        print('Please set OPENWEATHER_API_KEY environment variable')
        return

    app = WeatherApp(api_key)
    
    while True:
        city = input('Enter city name (or q to quit): ')
        if city.lower() == 'q':
            break

        result = app.get_weather(city)
        if 'error' in result:
            print(result['error'])
        else:
            print(f'\nWeather in {result["city"]}:')
            print(f'Temperature: {result["temperature"]}°C')
            print(f'Description: {result["description"]}')
            print(f'Humidity: {result["humidity"]}%')
            print(f'Last updated: {result["timestamp"]}\n')

if __name__ == '__main__':
    main()