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


TIME_SLOTS = pd.CategoricalDtype(
    categories=["09:00", "10:00", "11:00", "12:00"], ordered=True
)


COLUMN_TRANSFORMATIONS = {
    "species": "category",
    "sepal_length": "float64",
    "petal_length": "float64",
    "sepal_width": "float64",
    "petal_width": "float64",
    "test_int": "Int64",
    "test_string": "string",
    "time": pd.CategoricalDtype(
        categories=["10:00", "11:00", "09:00", "12:00"], ordered=True
    ),
}


@st.cache_data
def load_iris_data(nrows: int) -> pd.DataFrame:
    data = pd.read_csv(IRIS_DATA_LOCATION, nrows=nrows)
    data = data.assign(test_int=1, test_string="blahblahblah", time="10:00")
    columns = data.columns.tolist()
    data = data.assign(**{"": True})
    data = data[[""] + columns]
    data = data.astype(COLUMN_TRANSFORMATIONS)
    return data


st.title("Data-frame with type updates")
data = load_iris_data(100000)
data_updated = st.experimental_data_editor(
    data, use_container_width=True, key="experimental_data_editor", num_rows="dynamic"
)
st.subheader("Updated data-frame")
st.write(data_updated)
st.write(st.session_state.experimental_data_editor)
