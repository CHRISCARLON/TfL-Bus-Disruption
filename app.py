from tfl_read_parquet import read_parquet_and_ensure_list, merge_excel_with_df
from tfl_add_weightings import add_deciles_for_disruption_score
from tfl_bus_map import plot_routes
import streamlit as st
from streamlit_folium import folium_static


def main():
    st.set_page_config(layout="wide")
    st.title("TfL Bus Route Disruption Map")

    file_path = "final_bus_data.parquet"
    df = read_parquet_and_ensure_list(file_path)
    df_2 = merge_excel_with_df(df, "output.xlsx")
    df_3 = add_deciles_for_disruption_score(df_2)
    folium_map = plot_routes(df_3)
    folium_static(folium_map, width=1200, height=800)


if __name__ == "__main__":
    main()
