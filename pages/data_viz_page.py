import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from sample_API import *

# Create scenario directory if it doesn't exist
scenario_dir = Path("scenarios")
scenario_dir.mkdir(exist_ok=True)

st.title("Scenario configuration")
st.markdown("""Just a script for configuring the thingy""")

st.write("---")

df = get_data()

st.write(df)

chart = st.line_chart(df['ProductionLt100MW'][-10000:])
