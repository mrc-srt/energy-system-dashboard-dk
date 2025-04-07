import streamlit as st
from pathlib import Path

# Define page directory
home_path = Path("pages") / "home_page.py"
data_viz_path = Path("pages") / "data_viz_page.py"

# Define pages
home_page = st.Page(home_path, title="Homepage", icon= ":material/edit:")
data_viz_page = st.Page(data_viz_path, title="Data visualization")

# Set up navigation
pg = st.navigation(
    {
        "Home" : [home_page],
        "Data visualization": [data_viz_page],
        }
    )

# Run the selected page
st.set_page_config(page_title="Energidataservice API call",
                   layout="wide",
                   page_icon=":material/edit:")
pg.run()