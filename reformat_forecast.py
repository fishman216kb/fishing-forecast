import re
from datetime import datetime

with open("forecast.txt", "r") as f:
    raw_text = f.read()

# Extract the update timestamp
update_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# Remove attribution section (starting with "Source:")
raw_text = re.sub(r"\nSource:.*", "", raw_text, flags=re.DOTALL)

# Normalize line endings and split into lines
lines = raw_text.strip().splitlines()

# Initialize output HTML parts
html_parts = []

# Add the header line (zone)
html_parts.append(f"<strong>{lines[0]}</strong><br><br>")

# Format each line
in_forecast_section = False
for line in lines[1:]:
    line = line.strip()
    if not line:
        continue
    if re.match(r"^\.[A-Z ]+\.\.\.", line):
        html_parts.append(f"<br><strong>{line[1:]}</strong><br>")
        in_forecast_section = True
    elif in_forecast_section and line.startswith("."):
        html_parts.append(f"<br><strong>{line[1:]}</strong><br>")
    else:
        html_parts.append(f"{line}<br>")

# Extract temperatures
temps_match = re.search(
    r"The water temperature off Toledo is (\d+) degrees, off Cleveland (\d+)\s*degrees, and off Erie (\d+)\s*degrees\.",
    raw_text
)
if temps_match:
    toledo_temp, cleveland_temp, erie_temp = temps_match.groups()
    html_parts.append(f"<br><strong>Water temps:</strong><br>")
    html_parts.append(f"Toledo: {toledo_temp}°F<br>")
    html_parts.append(f"Cleveland: {cleveland_temp}°F<br>")
    html_parts.append(f"Erie: {erie_temp}°F<br>")

# Add update time
html_parts.append(f"<br><small>Last Update: {update_time}</small>")

# Combine and save
final_html = "\n".join(html_parts)
with open("forecast.html", "w") as f:
    f.write(final_html)
