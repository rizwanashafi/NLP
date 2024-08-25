from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
import pymysql  # Make sure pymysql is imported for MySQL connection

# Load environment variables
load_dotenv()

# Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()  # Clean the response

def read_sql_query(sql, host, port, username, password, database):
    try:
        connection = pymysql.connect(
            host=host,
            port=int(port),
            user=username,
            password=password,
            database=database
        )
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        connection.close()  # Ensure the connection is closed
        return rows
    except pymysql.MySQLError as e:  # Handle pymysql errors
        st.error(f"Database error: {e}")
        return []

# Define a more generalized prompt
prompt = [
    """
    You are an expert in converting English questions into SQL queries. The SQL database contains various tables with different columns.
    \nThe following is the description of the tables and columns in the database:
    - Table 1: {table_1_name} with columns: {table_1_columns}
    - Table 2: {table_2_name} with columns: {table_2_columns}
    - ...
    \nFor example,\nExample 1 - How many entries of records are present in {table_name}?, 
    the SQL command will be something like this SELECT COUNT(*) FROM {table_name} ;
    \nExample 2 - Tell me all records where {condition} in {table_name}?, 
    the SQL command will be something like this SELECT * FROM {table_name} 
    where {condition} ; 
    The SQL code should not have ``` in beginning or end and SQL word in output.
    """
]

# Streamlit App
st.set_page_config(page_title="SQL Query Retriever")
st.header("📊 Retrieve SQL Database App")

# Sidebar Inputs
st.sidebar.header("Database Connection Settings")
host = st.sidebar.text_input("Database Host (e.g., 127.0.0.1):", key="host")
port = st.sidebar.text_input("Database Port (e.g., 3306):", key="port")
username = st.sidebar.text_input("Database Username (e.g., root):", key="username")
password = st.sidebar.text_input("Database Password (e.g., root):", type="password", key="password")
database = st.sidebar.text_input("Database Name (e.g., students):", key="database")

# Main Area Input
question = st.text_input("Input your question:", key="input")
submit = st.button("Ask any question")

if submit:
    if host and port and username and password and database and question:
        # Generate SQL query from the question
        response = get_gemini_response(question, prompt)
        st.subheader("Generated SQL Query:")
        st.code(response)
        
        # Execute the query and display results
        response_data = read_sql_query(response, host, port, username, password, database)
        st.subheader("Query Results:")
        if response_data:
            for row in response_data:
                st.write(row)
        else:
            st.write("No results or error in query execution.")
    else:
        st.warning("Please enter all the required fields and a question.")