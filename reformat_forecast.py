# reformat_forecast.py

import re

def reformat_forecast(input_file='forecast.txt', output_file='formatted_forecast.txt'):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    reformatted = []
    water_temp_line = ""

    for line in lines:
        line = line.strip()

        # Skip line that refers to the open lakes forecast
        if line.startswith("See Lake Erie open lakes forecast"):
            continue

        # Capture water temperature line
        if line.startswith("The water temperature off"):
            water_temp_line = line
            continue

        # Add page break before new forecast periods (all uppercase, usually day names)
        if line.isupper() and any(keyword in line for keyword in [
            'TONIGHT', 'TODAY', 'SATURDAY', 'SUNDAY', 'MONDAY',
            'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']):
            reformatted.append("")  # Blank line to separate periods

        # Skip empty lines
        if line == "":
            continue

        reformatted.append(line)

    # Add reformatted water temperatures if available
    if water_temp_line:
        try:
            temps = {}
            # This regex captures patterns like "off City is 65" or "off City 65"
            matches = re.findall(r'off (\w+)(?: is)? (\d+)', water_temp_line)
            for city, temp in matches:
                temps[city] = temp

            if temps:
                reformatted.append("")  # Add space before temps
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

    # Write the final output
    with open(output_file, 'w') as f:
        for line in reformatted:
            f.write(line + '\n')

    print(f"Formatted forecast written to {output_file}")


if __name__ == "__main__":
    reformat_forecast()
