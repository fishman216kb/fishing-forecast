import re
from datetime import datetime

with open("forecast.txt", "r") as f:
    raw_text = f.read()

update_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# Remove attribution if present
raw_text = re.sub(r"\nSource:.*", "", raw_text, flags=re.DOTALL)

lines = raw_text.strip().splitlines()
html_parts = []

# Find and trim the first location line (e.g., Avon Point to Willowick OH-...)
location_line = ""
start_index = 0

for i, line in enumerate(lines):
    if "Avon Point to Willowick OH" in line:
        match = re.search(r"(.*?Willowick OH-)", line)
        if match:
            location_line = match.group(1)
        else:
            location_line = line  # fallback if format is unexpected
        start_index = i + 1
        break

if location_line:
    html_parts.append(f"<strong>{location_line}</strong><br><br>")

# Find first timestamp line (e.g., "1000 AM EDT Sun May 18 2025")
timestamp_pattern = re.compile(r"\d{3,4} (AM|PM) EDT")
while start_index < len(lines) and not timestamp_pattern.search(lines[start_index]):
    start_index += 1

# Start processing from the timestamp line
for line in lines[start_index:]:
    line = line.strip()
    if not line:
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
        html_parts[-1] = html_parts[-1].replace(
            '</div>\n</div>', f' {line}</div>\n</div>')
    else:
        html_parts.append(f"{line}<br>")

# Water temps
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

# Timestamp
html_parts.append(f"<br><small>Last Update: {update_time}</small>")

# Write output
with open("forecast.html", "w") as f:
    f.write("\n".join(html_parts))
