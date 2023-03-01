import logging
import pandas as pd
import streamlit as st
import st_df_extension.filter_dataframe as st_df_filter
from streamlit.elements.data_editor import (
    _apply_cell_edits,
    _apply_row_additions,
    _apply_row_deletions,
)

log = logging.getLogger(__name__)


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

Actually, a specialised filter is probably not needed in most cases. Easier is to just press `⌘ Cmd + F` or `Ctrl + F` to search for values, and then update those accordingly.
Specialised filters can be used for secondary display purposes, but these can be applied after the widget update feature.

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
st.write("Original number of rows: ", len(data))
data_filtered = st_df_filter.filter_dataframe(data, widget_key="filter_data")
st.dataframe(data_filtered)
st.header("Filter data that can be edited")
st.write("Original number of rows: ", len(data))
data_filtered_can_edit = st_df_filter.filter_dataframe(
    data, widget_key="filter_data_edit"
)
data_filtered_edited = st.experimental_data_editor(data_filtered_can_edit)
st.write("New number of rows: ", len(data_filtered_edited))
st.caption(
    "Note that filtered data is not re-filtered when values are edited. The reason is that the edited data-frame is not passed to the input filter. Only the original data-frame is passed. This also means that any edits will be lost when the filters are changed. Avoiding this behaviour will require using session state and on-change callbacks."
)
st.subheader("Edited data")
st.write(data_filtered_edited)
st.write("New number of rows: ", len(data_filtered_edited))


st.header(
    "Filter data that can be edited and edits are stored in session state (with multiple-edits bug)"
)
st.write("Original number of rows: ", len(data))
if "data_filtered_edit_maintained" not in st.session_state:
    st.session_state.data_filtered_edited = data.copy()
    data_filtered_edit_maintained = data.copy()
else:
    data_filtered_edit_maintained = st.session_state.data_filtered_edit_maintained

data_filtered_edit_maintained = st_df_filter.filter_dataframe(
    data_filtered_edit_maintained,
    widget_key="filter_widget_data_filtered_edit_maintained",
)
st.session_state.data_filtered_edit_maintained = st.experimental_data_editor(
    data_filtered_edit_maintained, key="edit_widget_data_filtered_edit_maintained"
)
st.caption(
    "Here we see that edits are propegated to the data-frame, but filtering is now permanent. We also see the anomoly where multiple data-frame edits in the same select session creates an odity where some edits."
)
st.write("New number of rows: ", len(st.session_state.data_filtered_edited))
st.subheader("Edited data")
st.write(st.session_state.data_filtered_edited)
st.caption(
    "And here we see that the edits haven't been reflected in the data-frame above."
)


st.header("Filter data that can be edited and edits are stored in session state")


def update_edit_maintained():
    log.info("Updating edit maintained")
    log.info(st.session_state.edit_widget_data_filtered_edit_maintained_v2)
    if "edited_cells" in st.session_state.edit_widget_data_filtered_edit_maintained_v2:
        edits = st.session_state.edit_widget_data_filtered_edit_maintained_v2[
            "edited_cells"
        ]
        _apply_cell_edits(st.session_state.data_filtered_edit_maintained_v2, edits)
    if "added_rows" in st.session_state.edit_widget_data_filtered_edit_maintained_v2:
        rows = st.session_state.edit_widget_data_filtered_edit_maintained_v2[
            "added_rows"
        ]
        _apply_row_additions(st.session_state.data_filtered_edit_maintained_v2, rows)
    if "deleted_rows" in st.session_state.edit_widget_data_filtered_edit_maintained_v2:
        rows = st.session_state.edit_widget_data_filtered_edit_maintained_v2[
            "deleted_rows"
        ]
        _apply_row_deletions(st.session_state.data_filtered_edit_maintained_v2, rows)


st.write("Original number of rows: ", len(data))
if "data_filtered_edit_maintained_v2" not in st.session_state:
    st.session_state.data_filtered_edit_maintained_v2 = data.copy()

data_filtered_edit_maintained_v2 = st_df_filter.filter_dataframe(
    st.session_state.data_filtered_edit_maintained_v2,
    widget_key="filter_widget_data_filtered_edit_maintained_v2",
)

st.experimental_data_editor(
    data_filtered_edit_maintained_v2,
    key="edit_widget_data_filtered_edit_maintained_v2",
    on_change=update_edit_maintained,
)
st.caption(
    """
The updates are shown in real-time in the filters, but the data-frame is refreshed each time, so changes in order, etc. is not respected.
"""
)
st.subheader("Edited data")
st.caption(
    """
Here we see that edits are not propegated in real team, and applied incorrectly.
Edits are done via an index value on `data_filtered_edit_maintained_v2`, not on `st.session_state.data_filtered_edit_maintained_v2`.
"""
)
st.write("New number of rows: ", len(st.session_state.data_filtered_edit_maintained_v2))

st.write(st.session_state.data_filtered_edit_maintained_v2)

# st.header(
#     "Filter data that can be edited and edits are stored in session state and original data is maintained."
# )
# if "data_filtered_edited" not in st.session_state:
#     st.session_state.data_filtered_edited = data.copy()
#     data_filtered_edit_maintained = data.copy()
# else:
#     data_filtered_edit_maintained = st.session_state.data_filtered_edited

# data_filtered_edit_maintained = st_df_filter.filter_dataframe(
#     data_filtered_edit_maintained, widget_key="filter_data_edit_maintained"
# )
# st.session_state.data_filtered_edited = st.experimental_data_editor(
#     data_filtered_edit_maintained, key="filter_data_edit_maintained"
# )
# st.caption(
#     "Here we see that edits are propegated to the data-frame, and filtering is no temporary, i.e. the edited data is back in the original data-frame."
# )
# st.subheader("Edited data")
# st.write(st.session_state.data_filtered_edited)
