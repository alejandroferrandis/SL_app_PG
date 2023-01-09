import streamlit as st
import psycopg2
import pandas as pd
import os
import sys
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrig.grid_options_builder import GridOptionsBuilder

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    # Connect to database #
    conn = None
    try:
        print("Connecting…")
        conn1 = psycopg2.connect(**st.secrets["postgres"])
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print("All good, Connection successful!")
    return conn1

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
#def run_query(query):
#    with conn.cursor() as cur:
#        cur.execute(query)
#        return cur.fetchall()


def sql_to_dataframe(conn, query, column_names):
   # 
   #Import data from a PostgreSQL database using a SELECT query 
   #
   cursor = conn.cursor()
   try:
      cursor.execute(query)
   except (Exception, psycopg2.DatabaseError) as error:
      print("Error: %s" % error)
   cursor.close()
   return 1
   # The execute returns a list of tuples:
   tuples_list = cursor.fetchall()
   cursor.close()
   # Now we need to transform the list into a pandas DataFrame:
   df = pd.DataFrame(tuples_list, columns=column_names)
   return df


#rows = run_query("SELECT * from fruit_list;")


st.title('Hello World')

# Print results.
#for row in rows:
#    st.write(f"{row}")

query = "SELECT * from fruit_list;"
column_names = ["ID","Fruit_list", "quantity", "value"]

df = sql_to_dataframe(conn, query, column_names)

df.head()

#closing the connection
conn.close()

df = sql_to_dataframe(conn, query, column_names)
