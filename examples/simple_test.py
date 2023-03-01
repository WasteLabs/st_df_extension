import pandas as pd
import streamlit as st
import st_df_extension.filter_dataframe as st_df_filter


IRIS_DATA_LOCATION = "tests/data/iris.csv"
UBER_DATE_COLUMN = "date/time"
UBER_DATA_LOCATION = (
    "https://s3-us-west-2.amazonaws.com/"
    "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)


@st.cache_data
def load_uber_data(nrows: int) -> pd.DataFrame:
    data = pd.read_csv(UBER_DATA_LOCATION, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data = data.assign(**{UBER_DATE_COLUMN: pd.to_datetime(data[UBER_DATE_COLUMN])})
    return data


@st.cache_data
def load_iris_data(nrows: int) -> pd.DataFrame:
    data = pd.read_csv(IRIS_DATA_LOCATION, nrows=nrows)
    return data


st.title("Design example")
st.markdown(
    """
    This is a design example for the st_df_extension package. 
    Some useful [data-frame features](https://docs.streamlit.io/library/api-reference/data/st.dataframe) are the following: 
* **Column sorting**: sort columns by clicking on their headers.
* **Column resizing**: resize columns by dragging and dropping column header borders.
* **Table (height, width) resizing**: resize tables by dragging and dropping the bottom right corner of tables.
* **Search**: search through data by clicking a table, using hotkeys (`⌘ Cmd + F` or `Ctrl + F`) to bring up the search bar, and using the search bar to filter data.
* **Copy to clipboard**: select one or multiple cells, copy them to clipboard, and paste them into your favorite spreadsheet software.
"""
)

st.header("Load data")
with st.spinner("Loading data..."):
    data = load_iris_data(100)
st.text("Loading data...done!")

st.header("Display raw data")
st.dataframe(data)
st.caption(
    "To search for values, click on the table and press `Cmd + F` (mac) or `Ctrl + F`."
)


st.header("Filter data")
data_filtered = st_df_filter.filter_dataframe(data, widget_key="filter_data")
st.dataframe(data_filtered)


st.header("Filter data that can be edited")
data_filtered_can_edit = st_df_filter.filter_dataframe(
    data, widget_key="filter_data_edit"
)
data_filtered_edited = st.experimental_data_editor(data_filtered_can_edit)
st.caption(
    "Note that filtered data is not re-filtered when values are edited. The reason is that the edited data-frame is not passed to the input filter. Only the original data-frame is passed."
)
st.subheader("Edited data")
st.write(data_filtered_edited)
