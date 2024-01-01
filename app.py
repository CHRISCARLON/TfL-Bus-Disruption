import streamlit as st
from tfl_read_parquet import read_parquet_and_ensure_list, merge_excel_with_df
from tfl_add_weightings import add_deciles_for_disruption_score
from tfl_bus_map import plot_routes
from streamlit_folium import folium_static


def title_page():
    st.markdown("# :bus: TfL Bus Route Disruption Map Version 1.1")
    st.warning("""
    Contains public sector information licensed under the Open Government Licence v3.0.
    **Data Sources:**
    - Street Manager permit data from March 2022 to April 2023.
    - TfL bus passenger data from March 2022 to April 2023.
    - TfL bus routes (Using TfL's open data API).
    """)
    st.markdown("""
    **Methodology:**
    - Filter permit data to include only "completed works in London". 
    - Assign permits a disruption score from 1-10 based on permit type (Minor, Standard, Major, Emergency, etc), 
      with Minor being the least disruptive and Major/Emergency being the most. 
    - Assign Bus routes a usage score based on total passenger numbers for the year 22/23. 
    - Place a 30m buffer around all bus routes.
    - Overlay permits with bus routes.
    - Calculate the number of permits falling within the buffer zone of each bus route. 
    - For each permit falling in the buffer zone of a bus route, multiply the bus route usage score by the permit
      disruption score.
    - Add these results to a "bus route disruption score" total for each bus route. 
    - Plot bus routes on a map with a color scale based on the bus route disruption score.
    """)
    st.markdown("""
    **Version 1 Features:**
    - Static Folium map displaying bus routes in London.
    - Layer control function allowing users to filter the map based on bus route disruption scores (Impact Levels).
    - Base map provided by OS Zoomstack for clear and detailed mapping.
    """)
    st.markdown("""
    **Version 2 Features:**
    - Use a different TfL source for bus routes: this will hopefully result in all bus routes having a data and will remove
    the black lines from the map. 
    - Differentiate between regular buses and night buses: for example, add an OS Zoomstack dark layer for night buses. 
    - Differentiate between numerous bus routes on the same road: create an option to easily 
cycle through them when clicked. 
    """)
    st.markdown("""
    **Version 3 Features:**
    - Stop treating bus routes as single blocks and calculate different levels of disruption at different sections of a bus
    route - some sections may be more impacted than others and this is an important distinction to make.
    """)


def map_page():
    file_path = "final_bus_data.parquet"
    df = read_parquet_and_ensure_list(file_path)
    df_2 = merge_excel_with_df(df, "output.xlsx")
    df_3 = add_deciles_for_disruption_score(df_2)
    folium_map = plot_routes(df_3)
    folium_static(folium_map, width=1200, height=1000)


def main():
    st.set_page_config(layout="wide")
    page = st.sidebar.radio("Please select a page", [":house: Home Page", ":world_map: Map Page"])

    if page == ":house: Home Page":
        title_page()
    elif page == ":world_map: Map Page":
        map_page()


if __name__ == "__main__":
    main()
