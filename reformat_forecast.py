# reformat_forecast.py

import re
from datetime import datetime

def reformat_forecast(input_file='forecast.txt', output_file='formatted_forecast.txt'):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    reformatted = []
    water_temp_line = ""
    forecast_period_regex = re.compile(r'^\.[A-Z]+')

    for line in lines:
        stripped = line.strip()

        # Preserve existing blank lines
        if stripped == "":
            reformatted.append("")
            continue

        # Skip open lakes line
        if stripped.startswith("See Lake Erie open lakes forecast"):
            continue

        # Capture water temp line
        if "The water temperature off" in stripped:
            water_temp_line = stripped
            continue

        # Add line break before new forecast period lines (e.g., .SUNDAY...)
        if forecast_period_regex.match(stripped):
            if reformatted and reformatted[-1] != "":
                reformatted.append("")

        reformatted.append(stripped)

    # Add parsed water temps
    if water_temp_line:
        try:
            # Find each city and the first two-digit number after it
            temps = {}
            for city in ['Toledo', 'Cleveland', 'Erie']:
                match = re.search(rf'{city}.*?(\d{{2}})', water_temp_line)
                if match:
                    temps[city] = match.group(1)

            if temps:
                reformatted.append("")
                reformatted.append("Water temps:")
                for city in ['Toledo', 'Cleveland', 'Erie']:
                    if city in temps:
                        reformatted.append(f"{city}: {temps[city]}°F")
        except Exception as e:
            reformatted.append("⚠️ Error parsing water temperatures.")
            print("Parsing error:", e)

    # Add source info
    reformatted.append("")
    reformatted.append("Source: NOAA / National Weather Service")
    reformatted.append("https://www.ndbc.noaa.gov/data/Forecasts/FZUS51.KCLE.html")

    # Add timestamp of last update
    now_utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    reformatted.append("")
    reformatted.append(f"Last Update: {now_utc}")

    # Write to file
    with open(output_file, 'w') as f:
        for line in reformatted:
            f.write(line + '\n')

    print(f"Formatted forecast written to {output_file}")

if __name__ == "__main__":
    reformat_forecast()
