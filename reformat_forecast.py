# reformat_forecast.py

def reformat_forecast(input_file='forecast.txt', output_file='formatted_forecast.txt'):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    reformatted = []
    water_temp_line = ""
    for line in lines:
        line = line.strip()

        # Skip Lake Erie open lakes forecast line
        if line.startswith("See Lake Erie open lakes forecast"):
            continue

        # Capture water temperature line
        elif line.startswith("The water temperature off"):
            water_temp_line = line
            continue

        # Keep other lines
        reformatted.append(line)

    # Reformat water temperature info
    if water_temp_line:
        try:
            temps = {
                'Toledo': water_temp_line.split('off Toledo is ')[1].split(' degrees')[0],
                'Cleveland': water_temp_line.split('off Cleveland ')[1].split(' degrees')[0],
                'Erie': water_temp_line.split('off Erie ')[1].split(' degrees')[0]
            }
            reformatted.append("")
            reformatted.append("Water temps:")
            reformatted.append(f"Toledo: {temps['Toledo']}°F")
            reformatted.append(f"Cleveland: {temps['Cleveland']}°F")
            reformatted.append(f"Erie: {temps['Erie']}°F")
        except Exception as e:
            reformatted.append("⚠️ Error parsing water temperatures.")
            print("Parsing error:", e)

    # Add source info
    reformatted.append("")
    reformatted.append("Source: NOAA / National Weather Service")
    reformatted.append("https://www.ndbc.noaa.gov/data/Forecasts/FZUS51.KCLE.html")

    # Write to output
    with open(output_file, 'w') as f:
        for line in reformatted:
            f.write(line + '\n')

    print(f"Formatted forecast written to {output_file}")

if __name__ == "__main__":
    reformat_forecast()
