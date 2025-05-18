import re
from datetime import datetime

with open("forecast.txt", "r") as f:
    raw_text = f.read()

update_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

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
        # Keep only "Avon Point to Willowick OH-" part and discard remainder of this line
        trimmed_location = "Avon Point to Willowick OH-"
        html_parts.append(f"<strong>{trimmed_location}</strong><br><br>")

        # Skip the next line after this one (so start from i+2)
        start_index = i + 2
        break

# Now process lines from start_index onwards
for line in lines[start_index:]:
    line = line.strip()
    if not line:
        continue
    # Detect timestamp line, just output it
    if re.match(r".*\d{1,2}(:\d{2})? ?(AM|PM)", line):
        html_parts.append(f"{line}<br>")
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

# Extract and format water temps (from the original raw text)
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
