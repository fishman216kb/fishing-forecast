import requests

url = "https://tgftp.nws.noaa.gov/data/raw/fz/fzus51.kcle.nsh.cle.txt"

def scrape_lez146_forecast():
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    text = response.text

    # Identify the start of the LEZ145>148 forecast block
    start_phrase = "LEZ145>148"
    start_idx = text.find(start_phrase)
    if start_idx == -1:
        print("Could not find LEZ145>148 forecast block.")
        return

    # Find where the block ends, which is marked by "$$"
    end_idx = text.find("$$", start_idx)
    if end_idx == -1:
        print("Could not find end of forecast block.")
        return

    # Extract the forecast block and preserve formatting
    forecast_block = text[start_idx:end_idx].strip()

    # Optionally, add attribution and formatting
    cleaned_forecast = (
        f"{forecast_block}\n\nSource: NOAA/National Weather Service"
    )

    # Save to file
    with open("forecast.txt", "w") as f:
        f.write(cleaned_forecast)

    print("Forecast saved successfully.")

if __name__ == "__main__":
    scrape_lez146_forecast()
