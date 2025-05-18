# reformat_forecast.py

import re

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
            # Match "off [City] [optional is] [temp] degrees"
            matches = re.findall(r'off (\w+)(?: is)? (\d+)', water_temp_line)
            temps = {city: temp for city, temp in matches}

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

    # Write to file
    with open(output_file, 'w') as f:
        for line in reformatted:
            f.write(line + '\n')

    print(f"Formatted forecast written to {output_file}")

if __name__ == "__main__":
    reformat_forecast()
