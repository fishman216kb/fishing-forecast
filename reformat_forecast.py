import re
from datetime import datetime

with open("forecast.txt", "r") as f:
    raw_text = f.read()

update_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# Remove attribution
raw_text = re.sub(r"\nSource:.*", "", raw_text, flags=re.DOTALL)

lines = raw_text.strip().splitlines()
html_parts = []

# Header
html_parts.append(f"<strong>{lines[0]}</strong><br><br>")
zone_done = False

# Process body
for line in lines[1:]:
    line = line.strip()
    if not line:
        continue

    # Stop processing after the "See Lake Erie open lakes forecast" line
    if line.lower().startswith("see lake erie open lakes forecast"):
        break

    # Additional zones
    if not zone_done and re.match(r".*\d+ (AM|PM)", line):
        html_parts.append(line + "<br>")
        zone_done = True
        continue

    # Forecast period header
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
        # Append to previous forecast-text line
        html_parts[-1] = html_parts[-1].replace(
            '</div>\n</div>', f' {line}</div>\n</div>')
    else:
        html_parts.append(f"{line}<br>")

# Extract and format water temps
temps_match = re.search(
    r"The water temperature off Toledo is (\d+) degrees, off Cleveland (\d+)\s*degrees, and off Erie (\d+)\s*degrees\.",
    raw_text
)
if temps_match:
    t, c, e = temps_match.groups()
    html_parts.append(f"""
<br><strong>Water temps:</strong><br>
Toledo: {t}°F<br>
Cleveland: {c}°F<br>
Erie: {e}°F<br>
    """)

html_parts.append(f"<br><small>Last Update: {update_time}</small>")

with open("forecast.html", "w") as f:
    f.write("\n".join(html_parts))
