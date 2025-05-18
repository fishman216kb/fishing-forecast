import re
from datetime import datetime

# Load raw forecast text
with open("raw_forecast.txt", "r") as f:
    raw_text = f.read()

# Extract water temps using simple city + number match
temp_matches = re.findall(r"(Toledo|Cleveland|Erie)[^\d]*(\d{2})", raw_text)
temps = {city: f"{temp}°F" for city, temp in temp_matches}

# Extract forecast body (everything before "The water temperature...")
forecast_body = raw_text.split("The water temperature")[0].strip()

# Build HTML forecast content
html_output = []

html_output.append('<section id="forecast">')

# Split into lines and convert to semantic blocks
for line in forecast_body.splitlines():
    line = line.strip()
    if line == "":
        continue
    if re.match(r"^[\.\.\.]*[A-Z ]+[\.\.\.]*$", line):
        # Emphasized alert line
        html_output.append(f'<p><strong>{line}</strong></p>')
    elif re.match(r"^\.[A-Z ]+\.\.\.", line):
        # Forecast period
        html_output.append(f'<h3>{line}</h3>')
    else:
        # Regular line
        html_output.append(f"<p>{line}</p>")

html_output.append("<h4>Water temps:</h4>")
html_output.append("<ul>")
for city in ["Toledo", "Cleveland", "Erie"]:
    if city in temps:
        html_output.append(f"<li><strong>{city}:</strong> {temps[city]}</li>")
html_output.append("</ul>")

html_output.append("""
<p>Source: NOAA / National Weather Service<br>
<a href="https://tgftp.nws.noaa.gov/data/raw/fz/fzus51.kcle.nsh.cle.txt" target="_blank">
NOAA Forecast Text Source</a></p>
""")

# Add timestamp
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
html_output.append(f'<small>Last Update: {timestamp}</small>')

html_output.append('</section>')

# Save to file
with open("forecast.html", "w") as f:
    f.write("\n".join(html_output))
