import requests

url = "https://tgftp.nws.noaa.gov/data/raw/fz/fzus51.kcle.nsh.cle.txt"

def scrape_weather():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        
        # Find the start of the section by searching for the specific text snippet
        start_index = data.find("Avon Point to Willowick OH")
        if start_index == -1:
            print("Could not find the forecast section for Avon Point to Willowick OH")
            return None
        
        # Find the end of this section marked by "$$" after the start index
        end_index = data.find("$$", start_index)
        if end_index == -1:
            # Just take till end of file if no $$ found
            end_index = len(data)
        
        forecast_section = data[start_index:end_index].strip()
        
        # Save to file
        with open('forecast.txt', 'w') as f:
            f.write(forecast_section)
        
        print("Forecast section saved to forecast.txt")
        return forecast_section
    else:
        print(f"Error fetching data: HTTP {response.status_code}")
        return None

if __name__ == "__main__":
    scrape_weather()
