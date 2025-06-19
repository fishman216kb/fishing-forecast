import re
from datetime import datetime
from zoneinfo import ZoneInfo

with open("forecast.txt", "r") as f:
    raw_text = f.read()

update_time = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %I:%M:%S %p %Z")

# Extract water temps before trimming anything
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
<note>There may be an issue with the lake temps from NWS, buoys are showing different readings</note><br>
"""

# Trim after "See Lake Erie open lakes forecast"
cutoff_match = re.search(r"See Lake Erie open lakes forecast", raw_text)
if cutoff_match:
    raw_text = raw_text[:cutoff_match.start()]

lines = raw_text.strip().splitlines()

html_parts = []

# Find and trim location line
start_index = 0
for i, line in enumerate(lines):
    if "Avon Point to Willowick OH" in line:
        trimmed_location = "Avon Point to Willowick OH-"
        html_parts.append(f"<strong>{trimmed_location}</strong><br><br>")
        # Find timestamp
        for j in range(i + 1, i + 4):
            if j < len(lines) and re.match(r".*\d{1,2}(:\d{2})? ?(AM|PM)", lines[j]):
                html_parts.append(f"{lines[j]}<br>")
                start_index = j + 1
                break
        break

# Process from start_index onward
advisory_text = ""
collecting_advisory = False
in_forecast_period = False

for line in lines[start_index:]:
    line = line.strip()
    if not line:
        continue

    # Handle advisory collection
    if line.startswith("...") and not collecting_advisory:
        collecting_advisory = True
        advisory_text = line + " "
        continue
    elif collecting_advisory:
        advisory_text += line + " "
        if line.endswith("..."):
            collecting_advisory = False
            advisory_text = advisory_text.strip()
            html_parts.append(f"<br><advisory>{advisory_text}</advisory><br>")
            advisory_text = ""
        continue

    # Handle forecast period start
    if line.startswith(".") and "..." in line:
        # Close previous if open
        if in_forecast_period:
            html_parts[-1] += "</div>\n</div>"
            in_forecast_period = False
        label, _, remainder = line[1:].partition("...")
        html_parts.append(f"""
<div class="forecast-period">
  <br>
  <div class="period-label"><dayheader>{label.strip()}</dayheader></div>
  <div class="period-text">{remainder.strip()}""")  # Leave open
        in_forecast_period = True
        continue

    # Handle continuation of forecast period
    if in_forecast_period:
        html_parts[-1] += ' ' + line
        continue

    # Anything else
    html_parts.append(f"{line}<br>")

# Close open forecast period at the very end if needed
if in_forecast_period:
    html_parts[-1] += "</div>\n</div>"

# Add water temps
html_parts.append(water_temps_html)

# Add timestamp and source
html_parts.append(
    f'<small>Last Update: {update_time}<br>'
    'Source: <a href="https://tgftp.nws.noaa.gov/data/raw/fz/fzus51.kcle.nsh.cle.txt" target="_blank">NOAA Marine Forecast</a></small>'
)

with open("forecast.html", "w") as f:
    f.write("\n".join(html_parts))
