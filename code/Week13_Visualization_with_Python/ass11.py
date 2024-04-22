import streamlit as st
import pandas as pd
import plotly.express as px


# Load the CSV data
@st.cache_data
def load_data():
    return pd.read_csv("rain.csv")


data = load_data()

data["date"] = pd.to_datetime(data["date"])

# Title
st.title("Rainfall Analysis")

# Sidebar
st.sidebar.header("Filter Options")
# Sidebar Widgets for controlling what's shown in the columns
province_option = st.sidebar.selectbox(
    "Select Province", data["province"].unique(), index=None
)

# Date filtering
min_date = data["date"].min()
max_date = data["date"].max()

start_date = st.sidebar.date_input(
    "Select Start Date",
    min_value=min_date,
    max_value=max_date,
    value=min_date,
)
end_date = st.sidebar.date_input(
    "Select End Date",
    min_value=start_date,
    max_value=max_date,
    value=max_date,
)

filtered_data = data[
    (data["date"] >= pd.to_datetime(start_date))
    & (data["date"] <= pd.to_datetime(end_date))
]
if province_option:
    filtered_data = data[data["province"] == province_option]


st.write("Daily Rainfall By Date", start_date, "and", end_date)
fig = px.bar(
    filtered_data,
    x="province",
    y="rain",
    color="tambon",
    title="Daily Rainfall",
    labels={"rain": "Rainfall (mm)"},
)
st.plotly_chart(fig)
# st.bar(filtered_data.groupby("province")["rain"].mean())

# Line chart showing daily rainfall
st.subheader("Daily Rainfall By Province")
fig = px.line(
    filtered_data,
    x="date",
    y="rain",
    color="province",
    title="Daily Rainfall",
    labels={"rain": "Rainfall (mm)"},
)
st.plotly_chart(fig)

# Map showing rainfall by location
st.subheader("Rainfall Map")


def create_animated_figure():
    fig = px.scatter_mapbox(
        filtered_data,
        lat="latitude",
        lon="longitude",
        animation_frame="datetime",
        animation_group="province",
        color="rain",
        size="rain",
        size_max=55,
        hover_name="tambon",
        hover_data=["rain", "date"],
        zoom=8,
    )
    fig.update_layout(mapbox_style="open-street-map", transition={"duration": 1000})
    return fig


st.plotly_chart(create_animated_figure())

# Summary statistics
highest_province = data.groupby("province")["rain"].mean().idxmax()
highest_date = data.groupby("date")["rain"].mean().idxmax()
lowest_province = data.groupby("province")["rain"].mean().idxmin()
lowest_date = data.groupby("date")["rain"].mean().idxmin()
st.subheader("Summary Statistics")
st.write(filtered_data.describe())
st.write(f"start_date: {start_date} end_date: {end_date}")
st.write(
    f"The province with the highest average rainfall is {highest_province} on {highest_date}"
)
st.write(
    f"The province with the lowest average rainfall is {lowest_province} on {lowest_date}"
)

st.header("Code Section")
file = "test.py"
with open(file, "r") as f:
    code = f.read()
st.code(code, language="python")
