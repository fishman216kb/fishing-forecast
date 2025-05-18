import re
from datetime import datetime

with open("forecast.txt", "r") as f:
    raw_text = f.read()

update_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# Trim beginning: Start with only "Avon Point to Willowick OH-"
start_match = re.search(r"Avon Point to Willowick OH-.*?\n", raw_text)
if start_match:
    trimmed_text = raw_text[start_match.end():]
    header_line = "<strong>Avon Point to Willowick OH-</strong><br><br>"
else:
    trimmed_text = raw_text
    header_line = ""

# Stop parsing at "See Lake Erie open lake"
stop_idx = trimmed_text.find("See Lake Erie open lake")
if stop_idx != -1:
    trimmed_text = trimmed_text[:stop_idx]

lines = trimmed_text.strip().splitlines()
html_parts = [header_line]

# Timestamp (first non-empty line)
for i, line in enumerate(lines):
    line = line.strip()
    if line:
        html_parts.append(f"{line}<br><br>")
        lines = lines[i+1:]
        break

# Small Craft Advisory (may be multiline)
advisory_lines = []
for i, line in enumerate(lines):
    if line.strip().startswith("..."):
        advisory_lines.append(line.strip())
    else:
        break

if advisory_lines:
    advisory_text = " ".join(advisory_lines)
    html_parts.append(f'<div style="color: red;"><strong>{advisory_text}</strong></div><br>')
    lines = lines[len(advisory_lines):]

# Forecast periods
forecast_started = False
for line in lines:
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
        forecast_started = True
    # Continuation of forecast text
    elif forecast_started and html_parts and 'forecast-period' in html_parts[-1]:
        html_parts[-1] = html_parts[-1].replace(
            '</div>\n</div>', f' {line}</div>\n</div>')
    else:
        html_parts.append(f"{line}<br>")

# Extract and display water temps if available
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
