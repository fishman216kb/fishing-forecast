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

    # Add parsed water temps using stricter matching
    if water_temp_line:
        try:
            cities = ['Toledo', 'Cleveland', 'Erie']
            temps = {}

            for city in cities:
                # Match city name followed by non-digits, then 1–2 digit number
                match = re.search(rf'{city}\D+?(\d{{1,2}})', water_temp_line)
                if match:
                    temps[city] = match.group(1)

            if temps
