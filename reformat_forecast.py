import re
from datetime import datetime

with open("forecast.txt", "r") as f:
    raw_text = f.read()

update_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# Remove attribution
raw_text = re.sub(r"\nSource:.*", "", raw_text, flags=re.DOTALL)

lines = raw_text.strip().splitlines()
html_parts = []

# Extract and format water temps early so we can delete the raw line
temps_match = re.search(
    r"The water temperature off Toledo is (\d+) degrees, off Cleveland (\d+)\s*degrees, and off Erie (\d+)\s*degrees\.",
    raw_text
)
water_temps_html = ""
if temps_match:
    t, c, e = temps_match.groups()
    water_temps_html = f"""
<br><strong>Water temps:</strong><br>
Toledo: {t}°F<br>
Cleveland: {c}°F<br>
Erie: {e}°F<br>
    """

# Trim everything before the first zone line
zone_line = next((line for line in lines if "Avon Point to Willowick OH" in line), None)
if zone_line:
    html_parts.append(f"<strong>{zone_line.strip()}</strong><br><br>")

# Skip lines until timestamp (e.g., "1000 AM EDT ...")
start_index = next((i for i, line in enumerate(lines) if re.match(r"\d{3,4} (AM|PM)", line)), None)
if start_index is None:
    start_index = 0  # fallback if no timestamp found

zone_done = False
for line in lines[start_index:]:
    line = line.strip()
    if not line:
        continue

    # Stop at "See Lake Erie open lakes forecast"
    if line.lower().startswith("see lake erie open lakes forecast"):
        break

    # Capture timestamp line
    if not zone_done and re.match(r"\d{3,4} (AM|PM)", line):
        html_parts.append(line + "<br>")
        zone_done = True
        continue

    # Forecast period headers
    if line.startswith(".") and "..." in line:
        label, _, remainder = line[1:].partition("...")
        html_parts.append(f"""
<div class="forecast-period">
  <div class="period-label">{label.strip()}</div>
  <div class="period-text">{remainder.strip()}</div>
</div>
        """)
    # Continuation of forecast text
    elif html_parts and 'forecast-period' in html_parts[-1]:
        html_parts[-1] = html_parts[-1].replace(
            '</div>\n</div>', f' {line}</div>\n</div>')
    else:
        html_parts.append(f"{line}<br>")

# Append cleaned water temps
if water_temps_html:
    html_parts.append(water_temps_html)

html_parts.append(f"<br><small>Last Update: {update_time}</small>")

with open("forecast.html", "w") as f:
    f.write("\n".join(html_parts))
