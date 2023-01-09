import streamlit as st
import psycopg2
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

st.title('Postgres AG Grid')

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query,column_names):
    with conn.cursor() as cur:
        cur.execute(query)
        tuples_list = cur.fetchall()
        df = pd.DataFrame(tuples_list, columns=column_names)
        return df

column_names = ["ID","Fruit","Quantity","Price"]    

df = run_query("SELECT * from fruit_list;",column_names)

st.header("This is a Df")
# Print results.
st.dataframe(df)

st.header("This is AG Grid")
AgGrid(df)
