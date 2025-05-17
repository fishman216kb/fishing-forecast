import requests
import re

url = "https://tgftp.nws.noaa.gov/data/raw/fz/fzus51.kcle.nsh.cle.txt"

def parse_forecast(text):
    # Isolate the LEZ146 zone forecast
    start = text.find("Avon Point to Willowick OH")
    end = text.find("$$", start)
    if start == -1 or end == -1:
        return "Forecast zone not found."

    zone_text = text[start:end].strip()

    # Break into periods by uppercase headers (TONIGHT, SUNDAY, etc.)
    periods = re.split(r'\n(?=[A-Z][A-Z ]+\n)', zone_text)
    output_lines = []

    for period in periods:
        lines = period.strip().split('\n')
        if not lines or len(lines) < 2:
            continue

        title = lines[0].strip()
        body = ' '.join(lines[1:]).replace('\n', ' ').strip()

        # Extract wind and wave sentences
        wind = wave = ''
        wind_match = re.search(r'(winds?[^.]+?\.)', body, re.IGNORECASE)
        wave_match = re.search(r'(waves?[^.]+?\.)', body, re.IGNORECASE)

        if wind_match:
            wind = "Wind: " + wind_match.group(1).strip()
        if wave_match:
            wave = "Waves: " + wave_match.group(1).strip()

        # Add to output
        output_lines.append(title)
        if wind:
            output_lines.append(wind)
        if wave:
            output_lines.append(wave)
        output_lines.append('')  # blank line for spacing

    # Add attribution
    output_lines.append("Source: NOAA/National Weather Service")

    return '\n'.join(output_lines)

def save_forecast_to_file(forecast_text, filename="forecast.txt"):
    with open(filename, "w") as f:
        f.write(forecast_text)

def main():
    response = requests.get(url)
    if response.status_code == 200:
        parsed_forecast = parse_forecast(response.text)
        save_forecast_to_file(parsed_forecast)
        print("Forecast saved to forecast.txt")
    else:
        print(f"Error fetching forecast: {response.status_code}")

if __name__ == "__main__":
    main()
