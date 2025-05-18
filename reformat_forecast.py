import re
from datetime import datetime
from zoneinfo import ZoneInfo

with open("forecast.txt", "r") as f:
    raw_text = f.read()

update_time = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %I:%M:%S %p %Z")

# Extract water temps from the original raw text BEFORE trimming
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

# Cut off everything after the "See Lake Erie open lakes forecast" line
cutoff_match = re.search(r"See Lake Erie open lakes forecast", raw_text)
if cutoff_match:
    raw_text = raw_text[:cutoff_match.start()]

lines = raw_text.strip().splitlines()

html_parts = []

# Find and trim the location line
start_index = 0
for i, line in enumerate(lines):
    if "Avon Point to Willowick OH" in line:
        trimmed_location = "Avon Point to Willowick OH-"
        html_parts.append(f"<strong>{trimmed_location}</strong><br><br>")
        # Skip the next line after this one (start at i+2)
        start_index = i + 2
        break

# Process lines from start_index
for line in lines[start_index:]:
    line = line.strip()
    if not line:
        continue
    if re.match(r".*\d{1,2}(:\d{2})? ?(AM|PM)", line):
        html_parts.append(f"{line}<br>")
        continue
    if line.startswith(".") and "..." in line:
        label, _, remainder = line[1:].partition("...")
        html_parts.append(f"""
<div class="forecast-period">
  <div class="period-label">{label.strip()}</div>
  <div class="period-text">{remainder.strip()}</div>
</div>
""")
    elif html_parts and 'forecast-period' in html_parts[-1]:
        html_parts[-1] = html_parts[-1].replace(
            '</div>\n</div>', f' {line}</div>\n</div>')
    else:
        html_parts.append(f"{line}<br>")

# Add back the water temps html block
html_parts.append(water_temps_html)

# Add last update timestamp
html_parts.append(f"<br><small>Last Update: {update_time}</small>")

with open("forecast.html", "w") as f:
    f.write("\n".join(html_parts))
