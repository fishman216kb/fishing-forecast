import requests
from bs4 import BeautifulSoup

url = "https://tgftp.nws.noaa.gov/data/raw/fz/fzus51.kcle.nsh.cle.txt"

def scrape_weather():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        start = data.find("Avon Point to Willowick OH")
        end = data.find("See Lake Erie open lakes forecast", start)
        weather_info = data[start:end].strip()
        print(f"Weather Info:\n{weather_info}")
        return weather_info
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    scrape_weather()
