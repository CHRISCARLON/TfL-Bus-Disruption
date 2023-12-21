from tfl_read_parquet import read_parquet_and_ensure_list, merge_excel_with_df
from tfl_add_weightings import add_deciles_for_disruption_score
from tfl_bus_map import plot_routes
import streamlit as st
from streamlit_folium import folium_static


def main():
    st.set_page_config(layout="wide")
    st.title("TfL Bus Route Disruption Map (Version 1.0)")
    st.markdown("""
    **Data Sources:**
    - Street Manager permit data from March 2022 to April 2023.
    - TfL bus passenger data from March 2022 to April 2023.
    - TfL bus routes (Using TfL's open data API).
    """)
    st.markdown("""
    **Methodology:**
    - Filter permit data to include only "completed works in London". 
    - Assign permits a disruption score from 1-10 based on permit type (Minor, Standard, Major, Emergency, etc) - 
    with Minor being the least disruptive and Major/Emergency being the most. 
    - Assign Bus routes a usage score based on total passenger numbers for the year 22/23. 
    - Place a 30m buffer around all bus routes.
    - Overlay permits with bus routes.
    - Calculate the number of permits falling within the buffer zone of each bus route. 
    - For each permit falling in the buffer zone of a bus route **multiply the bus route usage score by the permit
    disruption score**.
    - Add these results to a "bus route disruption score" total for each bus route. 
    - Plot bus routes on a map. 
    - Set a colour scale and colour bus routes based on bus route disruption score.
    """)
    st.markdown("""
    **Version 1 Features:**
    - Static folium map 
    - Layer control function: filter the map based on the bus route disruption scores (called Impact Levels on the map)
    - OS Zoomstack base map
    """)

    file_path = "final_bus_data.parquet"
    df = read_parquet_and_ensure_list(file_path)
    df_2 = merge_excel_with_df(df, "output.xlsx")
    df_3 = add_deciles_for_disruption_score(df_2)
    folium_map = plot_routes(df_3)
    folium_static(folium_map, width=1300, height=850)


if __name__ == "__main__":
    main()
