import requests

url = "https://tgftp.nws.noaa.gov/data/raw/fz/fzus51.kcle.nsh.cle.txt"


def fetch_buoy_data():
    # Replace with the correct endpoint for the Rocky River buoy
    url = 'https://limno.io/api/now/45196'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        water_temp = data.get('waterTemperature')
        wave_height = data.get('waveHeight')
        print(f'Water Temp: {water_temp}°F, Wave Height: {wave_height} ft')
        return water_temp, wave_height
    else:
        print(f'Error fetching data: {response.status_code}')
        return None, None

if __name__ == "__main__":
    fetch_buoy_data()




def scrape_weather():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        start = data.find("Avon Point to Willowick OH")
        end = data.find("$$", start)
        weather_info = data[start:end].strip()
        
        # Save the weather information to a file
        with open('forecast.txt', 'w') as f:
            f.write(f"Weather Info:\n{weather_info}")
        
        return weather_info
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    scrape_weather()
