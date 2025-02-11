from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)

# Load CSV data
file_path = "static/sensor_data.csv"  # Place CSV inside the 'static' folder
df = pd.read_csv(file_path)

def create_charts():
    """Generate visualizations with professional styling, informative labels, tooltips, and interactive features."""
    custom_template = "plotly_white"
    
    # Accelerometer Data Plot
    fig_acc = px.line(df, x=df.index, y=['accelerometer_x', 'accelerometer_y', 'accelerometer_z'],
                      title="Accelerometer Data Over Time",
                      labels={'value': 'Acceleration (m/s²)', 'index': 'Time (Index)'} ,
                      template=custom_template)
    fig_acc.update_traces(mode='markers+lines')
    fig_acc.update_layout(margin=dict(l=20, r=20, t=50, b=20), title_x=0.5)
    acc_graph = fig_acc.to_html(full_html=False)
    
    # Gyroscope Data Plot
    fig_gyro = px.line(df, x=df.index, y=['gyroscope_x', 'gyroscope_y', 'gyroscope_z'],
                       title="Gyroscope Data Over Time",
                       labels={'value': 'Rotation Speed (rad/s)', 'index': 'Time (Index)'},
                       template=custom_template)
    fig_gyro.update_traces(mode='markers+lines')
    fig_gyro.update_layout(margin=dict(l=20, r=20, t=50, b=20), title_x=0.5)
    gyro_graph = fig_gyro.to_html(full_html=False)
    
    # Location Heatmap
    fig_map = px.scatter_mapbox(df, lat="location_latitude", lon="location_longitude", zoom=10,
                                title="GPS Location Tracking", mapbox_style="carto-positron",
                                labels={'location_latitude': 'Latitude', 'location_longitude': 'Longitude'})
    fig_map.update_layout(margin=dict(l=20, r=20, t=50, b=20), title_x=0.5)
    map_graph = fig_map.to_html(full_html=False)
    
    # Battery Level Over Time
    fig_battery = px.line(df, x=df.index, y='battery_batteryLevel',
                           title="Battery Level Over Time",
                           labels={'battery_batteryLevel': 'Battery Level (%)', 'index': 'Time (Index)'},
                           template=custom_template)
    fig_battery.update_traces(mode='markers+lines')
    fig_battery.update_layout(margin=dict(l=20, r=20, t=50, b=20), title_x=0.5)
    battery_graph = fig_battery.to_html(full_html=False)
    
    # Histogram of Sensor Readings Distribution
    fig_hist = px.histogram(df, x=['accelerometer_x', 'accelerometer_y', 'accelerometer_z'],
                             title="Distribution of Accelerometer Readings",
                             labels={'value': 'Acceleration (m/s²)'}, template=custom_template)
    fig_hist.update_layout(barmode='overlay')
    hist_graph = fig_hist.to_html(full_html=False)
    
    return acc_graph, gyro_graph, map_graph, battery_graph, hist_graph

@app.route('/')
def dashboard():
    """Render the dashboard page with explanations, labels, tooltips, and enhanced usability."""
    acc_graph, gyro_graph, map_graph, battery_graph, hist_graph = create_charts()
    return render_template('dashboard.html', acc_graph=acc_graph, gyro_graph=gyro_graph, 
                           map_graph=map_graph, battery_graph=battery_graph, hist_graph=hist_graph,
                           page_title="IoT Sensor Data Dashboard",
                           description="This dashboard visualizes sensor data collected from a smartphone, providing insights into movement, location, and device status.")

if __name__ == '__main__':
    app.run(debug=True)
