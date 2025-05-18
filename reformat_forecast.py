import re
from datetime import datetime

def reformat_forecast(input_file='forecast.txt', output_file='formatted_forecast.txt'):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    reformatted = []
    water_temp_text = ""
    forecast_period_regex = re.compile(r'^\.[A-Z]+')

    # First, join lines so we can extract multi-line water temp text reliably
    full_text = "".join(lines)

    # Extract the water temperature sentence from the whole text (greedy match)
    water_temp_match = re.search(r'The water temperature off.*?degrees\.', full_text, re.DOTALL)
    if water_temp_match:
        water_temp_text = water_temp_match.group(0).replace('\n', ' ').strip()

    for line in lines:
        stripped = line.strip()

        # Preserve blank lines
        if stripped == "":
            reformatted.append("")
            continue

        # Skip open lakes line
        if stripped.startswith("See Lake Erie open lakes forecast"):
            continue

        # Skip water temperature lines because we add formatted temps later
        if "The water temperature off" in stripped or "degrees." in stripped:
            continue

        # Add line break before new forecast period lines (e.g., .SUNDAY...)
        if forecast_period_regex.match(stripped):
            if reformatted and reformatted[-1] != "":
                reformatted.append("")

        reformatted.append(stripped)

    # Parse water temps from the combined water_temp_text
    if water_temp_text:
        try:
            # Find each city followed by 1 or 2 digits (whole number temp)
            temps = {}
            for city in ['Toledo', 'Cleveland', 'Erie']:
                pattern = city + r'\D+(\d{1,2})'
                match = re.search(pattern, water_temp_text)
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

    # Add timestamp for last update in UTC
    reformatted.append("")
    reformatted.append(f"Last Update: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")

    # Write output file
    with open(output_file, 'w') as f:
        for line in reformatted:
            f.write(line + '\n')

    print(f"Formatted forecast written to {output_file}")

if __name__ == "__main__":
    reformat_forecast()
