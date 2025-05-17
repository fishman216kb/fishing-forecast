import requests
import re

url = "https://tgftp.nws.noaa.gov/data/raw/fz/fzus51.kcle.nsh.cle.txt"

def extract_forecast_for_lez146(text):
    # Define the LEZ146 zone section
    pattern = r"LEZ145>148-.*?(?=\n\n|\Z)"  # Match from LEZ145>148 to the next double newline
    match = re.search(pattern, text, re.DOTALL)
    
    if not match:
        return "Could not find forecast for LEZ146."
    
    # Extract and clean the section
    section = match.group(0)
    
    # Optionally clean "$$" or trailing metadata
    section = section.split("$$")[0].strip()
    return section

def save_forecast():
    response = requests.get(url)
    if response.status_code == 200:
        raw_text = response.text
        forecast = extract_forecast_for_lez146(raw_text)

        # Save to file
        with open('forecast.txt', 'w') as f:
            f.write(forecast)

        print("✅ Forecast extracted and saved.")
        print("\n--- Forecast Preview ---\n")
        print(forecast)
    else:
        print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    save_forecast()
