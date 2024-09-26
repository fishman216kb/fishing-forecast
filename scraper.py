import requests

url = "https://tgftp.nws.noaa.gov/data/raw/fz/fzus51.kcle.nsh.cle.txt"

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
