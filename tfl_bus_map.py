import folium
from folium.plugins import FloatImage
from datetime import datetime
import math
import branca
import streamlit as st


def is_jump(coord1, coord2, km_threshold):
    """
    Checks if there's a significant jump in distance between two points.
    """
    # Convert threshold from kilometers to degrees latitude
    threshold_degrees = km_threshold / 111
    lat_diff = abs(coord1[0] - coord2[0])
    # Calculate the corresponding threshold in degrees longitude at this latitude
    lon_threshold_degrees = threshold_degrees / math.cos(math.radians((coord1[0] + coord2[0]) / 2))
    lon_diff = abs(coord1[1] - coord2[1])
    return lat_diff > threshold_degrees or lon_diff > lon_threshold_degrees


def plot_routes(df, map_center=(51.509865, -0.118092), zoom_start=12, jump_threshold_km=1.5):
    """
    Plots routes from a DataFrame on a Folium map using decile groupings for color gradients.
    """

    # Create folium map
    route_map = folium.Map(location=map_center, min_zoom=7, max_zoom=16, tiles=None)

    # API key and layer for OS' Data Hub
    key = st.secrets.os_key
    layer = 'Light_3857'

    # Construct OS Maps ZXY API path with API key
    zxy_path = f'https://api.os.uk/maps/raster/v1/zxy/{layer}/{{z}}/{{x}}/{{y}}.png?key={key}'

    # Current date-time to include in the attribution
    date = datetime.now()

    # Add the OS base map as a separate tile layer, set to be visible but not in layer control
    folium.TileLayer(tiles=zxy_path, attr=f'Contains OS Data © Crown Copyright and Database Right {date.year}',
                     control=False, show=True).add_to(route_map)

    # Add OS logo to the map
    logo_url = 'https://labs.os.uk/public/os-api-branding/v0.1.0/img/os-logo-maps.svg'
    FloatImage(logo_url, bottom=1, left=1).add_to(route_map)

    # Create colour map for plotting weighted bus routes
    color_map = {
        'Impact Level 1': '#8dd35f',  # Light Green
        'Impact Level 2': '#a8d96c',  # Green-Yellow
        'Impact Level 3': '#c3df7a',  # Yellow-Green
        'Impact Level 4': '#ded488',  # Yellow
        'Impact Level 5': '#f9ca96',  # Orange-Yellow
        'Impact Level 6': '#f4b07b',  # Light Orange
        'Impact Level 7': '#ef9661',  # Orange
        'Impact Level 8': '#ea7a47',  # Red-Orange
        'Impact Level 9': '#e55d2e',  # Red
        'Impact Level 10': '#e0401c',  # Dark Red
        'No Data or Zero Impact Level Calculated': '#28282B'  # Black
    }

    # Create a branca colormap object
    colormap = branca.colormap.LinearColormap(
        colors=list(color_map.values()),
        index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        vmin=1,
        vmax=10,
        caption='Bus Route Impact Levels (Lowest to Highest): Use Filter to Control Layers'
    )

    # Add the colormap to the map
    route_map.add_child(colormap)

    # Create feature groups for each deciles group and add them to the map
    group_layers = {group: folium.FeatureGroup(name=f'{group}') for group in color_map}
    for group in group_layers:
        group_layers[group].add_to(route_map)

    # Iterate through the DataFrame and plot each route
    for index, row in df.iterrows():
        # Make sure 'lineStrings' column contains the expected format of line strings
        if isinstance(row['lineStrings'], list) and len(row['lineStrings']) > 1:
            # Initialize a new segment
            segments = []
            current_segment = [row['lineStrings'][0]]

            # Iterate over the line string points
            for i in range(1, len(row['lineStrings'])):
                if is_jump(row['lineStrings'][i - 1], row['lineStrings'][i], jump_threshold_km):
                    # Finish the current segment and start a new one if there's a jump
                    segments.append(current_segment)
                    current_segment = [row['lineStrings'][i]]
                else:
                    # Otherwise, continue adding points to the current segment
                    current_segment.append(row['lineStrings'][i])
            # Add the last segment if it's not empty
            if current_segment:
                segments.append(current_segment)

            # Determine the decile group and corresponding feature group
            decile_group = row.get('Score_Decile_Group', 'No Data or Zero')
            feature_group = group_layers.get(decile_group, route_map)

            # Plot each segment separately
            for segment in segments:
                popup_text = (f"Route Name: {row['name']} - Route Section: {row['route_section_name']} - "
                              f"Decile Group: {decile_group}")
                popup = folium.Popup(popup_text, parse_html=True)
                folium.PolyLine(
                    segment,
                    color=color_map[decile_group],
                    weight=2.5,
                    opacity=1,
                    popup=popup  # Add the popup to the PolyLine
                ).add_to(feature_group)
        else:
            print(f"Skipping row {index}, does not contain valid 'lineStrings' data")

    # Add layer control to toggle between deciles groups
    folium.LayerControl().add_to(route_map)

    return route_map
