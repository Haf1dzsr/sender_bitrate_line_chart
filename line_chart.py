from bokeh.plotting import figure, show, output_file
from bokeh.models import DatetimeTickFormatter, DatetimeTicker
from datetime import datetime
import re

file_path = 'soal_chart_bokeh.txt'

with open(file_path, 'r') as file:
    data = file.readlines()

# regex pattern
timestamp_pattern = r"Timestamp: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
speed_pattern = r"\[\s*\d+\]   \d+\.\d+-\d+\.\d+  sec\s+\d+\.?\d*\s+\w+Bytes\s+(\d+\.?\d*)\s+([KM])bits/sec\s+\d+\s+sender"

timestamps = []
speeds = []

for line in data:
    timestamp_match = re.search(timestamp_pattern, line)
    if timestamp_match:
        timestamps.append(timestamp_match.group(1))
    
    speed_match = re.search(speed_pattern, line)
    if speed_match:
        bitrate_value = float(speed_match.group(1))

        unit = speed_match.group(2)

        # Convert Kbits to Mbits
        if unit == 'K':
            bitrate_value = bitrate_value / 1000

        speeds.append(bitrate_value)

# Convert timestamp to datetime
timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in timestamps]

# create figure
p = figure(title="Testing Jaringan", x_axis_label='DATE TIME', y_axis_label='Speed (Mbps)', x_axis_type='datetime', width=900, height=400)

# line chart
p.line(timestamps, speeds, line_width=2, color='blue', legend_label="Speed (Mbps)")

# X label format
p.xaxis.formatter = DatetimeTickFormatter(days="%m/%d/%Y\n%H:%M:%S")
p.xaxis.ticker = DatetimeTicker(desired_num_ticks=11)

# Font style
p.title.text_font_size = '18pt'   
p.title.text_font_style = 'bold'  

p.xaxis.axis_label_text_font_size = '14pt'  
p.xaxis.axis_label_text_font_style = 'normal' 

p.yaxis.axis_label_text_font_size = '14pt'  
p.yaxis.axis_label_text_font_style = 'normal'   

output_file("line_chart.html")

show(p)