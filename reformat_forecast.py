import re
from datetime import datetime
from zoneinfo import ZoneInfo

# Read raw forecast
with open("forecast.txt", "r") as f:
    raw_text = f.read()

update_time = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %I:%M:%S %p %Z")

# Extract water temps BEFORE trimming
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
<note>There may be an issue with the lake temps from NOAA, buoys are showing different readings</note><br>
"""

# Trim everything after the "Winds and waves higher" or "See Lake Erie open lakes forecast" lines
cutoff_matchA = re.search(r"Winds and waves higher", raw_text)
cutoff_matchB = re.search(r"See Lake Erie open lakes forecast", raw_text)
if cutoff_matchA:
    raw_text = raw_text[:cutoff_matchA.start()]
elif cutoff_matchB:
    raw_text = raw_text[:cutoff_matchB.start()]

lines = raw_text.strip().splitlines()
html_parts = []

# Find and trim the location line
start_index = 0
for i, line in enumerate(lines):
    if "Avon Point to Willowick OH" in line:
        trimmed_location = "Avon Point to Willowick OH-"
        html_parts.append(f"<strong>{trimmed_location}</strong><br><br>")
        # Look for timestamp within next 3 lines
        for j in range(i + 1, i + 4):
            if j < len(lines) and re.match(r".*\d{1,2}(:\d{2})? ?(AM|PM|EDT|EST)", lines[j]):
                html_parts.append(f"{lines[j]}<br>")
                start_index = j  # Start here to allow advisory detection immediately after
                break
        break

# Advisory detection variables
advisory_text = ""
collecting_advisory = False
in_forecast_period = False

# Process lines
for line in lines[start_index + 1:]:  # Start after timestamp line
    line = line.strip()
    if not line:
        continue

    # --- Advisory Detection ---
    if line.startswith("...") and not collecting_advisory:
        collecting_advisory = True
        advisory_text = line + " "
        # If advisory ends on the same line (starts and ends with '...')
        if line.endswith("..."):
            collecting_advisory = False
            advisory_text = advisory_text.strip()
            html_parts.append(f'<br><advisory>{advisory_text}</advisory><br>')
            advisory_text = ""
        continue
    elif collecting_advisory:
        advisory_text += line + " "
        if line.endswith("..."):
            collecting_advisory = False
            advisory_text = advisory_text.strip()
            html_parts.append(f'<br><advisory>{advisory_text}</advisory><br>')
            advisory_text = ""
        continue  # Skip further processing while collecting advisory

    # --- Forecast Period Detection ---
    if line.startswith(".") and "..." in line:
        label, _, remainder = line[1:].partition("...")
        html_parts.append(f"""
<div class="forecast-period">
  <br>
  <div class="period-label"><dayheader>{label.strip()}</dayheader></div>
  <div class="period-text">{remainder.strip()}""")
        in_forecast_period = True
        continue

    # Continuation of a forecast period
    if in_forecast_period:
        # Check if the next line is starting a new period
        if line.startswith(".") and "..." in line:
            html_parts[-1] += "</div>\n</div>"
            label, _, remainder = line[1:].partition("...")
            html_parts.append(f"""
<div class="forecast-period">
  <br>
  <div class="period-label"><dayheader>{label.strip()}</dayheader></div>
  <div class="period-text">{remainder.strip()}""")
        else:
            html_parts[-1] += ' ' + line
        continue

    # If forecast period unexpectedly ended
    if in_forecast_period:
        html_parts[-1] += "</div>\n</div>"
        in_forecast_period = False

    # Any other line
    html_parts.append(f"{line}<br>")

# Close last forecast period if open
if in_forecast_period:
    html_parts[-1] += "</div>\n</div>"

# Add water temps block
html_parts.append(water_temps_html)

# Add update time
html_parts.append(
    f'<small>Last Update: {update_time}<br>'
    'Source: <a href="https://tgftp.nws.noaa.gov/data/raw/fz/fzus51.kcle.nsh.cle.txt" target="_blank">NOAA Marine Forecast</a></small>'
)

# Write to output
with open("forecast.html", "w") as f:
    f.write("\n".join(html_parts))
