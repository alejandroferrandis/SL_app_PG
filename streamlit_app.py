import streamlit as st
import psycopg2
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode
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

_funct = st.sidebar.radio(label="Functions", options = ['Display', 'Highlight'])
st.header("This is AG Grid")

gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_pagination(enabled=True)
gd.configure_default_column(editable=True, groupable=True)

if _funct == 'Display':    
    sel_mode = st.radio('Selection Type', options = ['single', 'multiple'])
    gd.configure_selection(selection_mode=sel_mode, use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(df,
                        gridOptions=gridoptions, 
                        update_mode= GridUpdateMode.SELECTION_CHANGED, 
                        height=500,
                        width='100%',
                        allow_unsafe_jscode=True)

    st.header('Output')

    sel_row = grid_table["selected_rows"]
    st.write(sel_row)

    
if _funct == 'Highlight': 
    col_opt = st.selectbox(label='Select column',options = df.columns)
    cellstyle_jscode = JsCode("""
        function(params){
        if (params.value == 'apple') {
            return {
                'color': 'black',
                'backgroundColor': 'orange'
        }
        }
        
        
    };
    """)
    
    gd.configure_columns(col_opt, cellStyle=cellstyle_jscode)
    gridOptions = gd.build()
    grid_table = AgGrid(df,
                        gridOptions = gridOptions,
                        enable_enterprise_modules = True,
                        fit_columns_on_grid_load = True,
                        height = 500,
                        width = '100%',
                        theme = "material",
                        update_mode = GridUpdateMode.SELECTION_CHANGED,
                        reload_data = True,
                        allow_unsafe_jscode=True
                        )
