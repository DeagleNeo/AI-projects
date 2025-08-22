import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import pymysql
import json

load_dotenv()
#os.environ["http_proxy"] = "http://127.0.0.1:1083"
#os.environ["https_proxy"] = "http://127.0.0.1:1083"

client = OpenAI()

# Access the Database configuration from the environment variables
host = os.getenv("HOST")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")

def get_completion(table_schema, sql_requirements, model="gpt-4o", temperature=0):
    instruction = """
            You are a professional SQL engineer, adept at generating SQL query based on the given schema and user input. Please generate SQL query based on the following requirements:
        """
  
    examples = """
            Table schema as below:
            orders (
                id INT PRIMARY KEY NOT NULL,
                customer_id INT NOT NULL,
                product_id VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                STATUS INT NOT NULL CHECK (STATUS IN (0, 1, 2)),
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                pay_time TIMESTAMP NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            );

            customers (
                id INT PRIMARY KEY NOT NULL,
                customer_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE,
                register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            products (
                id INT PRIMARY KEY NOT NULL,
                product_name VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL
            );
            User input:
            Which customer has the highest total expenditure? How much is it?
            Generated SQL query:
            SELECT customer_id, SUM(price) AS total_expense FROM orders GROUP BY customer_id ORDER BY total_expense DESC LIMIT 1;
        """
    prompt = f"""
            {instruction}
            Example:
            {examples}
            Table schema as below:
            {table_schema}

            User input:
            {sql_requirements}
        """
    print(prompt)

    
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content

def get_all_create_table_statements(host, user, password, database):
    try:
        # Connect to MySQL Database
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()

        # Get all tables from database
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        create_statements = []

        # Iterate all tables and get table creation statements
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SHOW CREATE TABLE `{table_name}`;")
            create_statement = cursor.fetchone()[1]
            create_statements.append(create_statement)

        # Close the cursor and the database connection
        cursor.close()
        conn.close()

        return json.dumps(create_statements, indent=4, ensure_ascii=False)

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return None

st.title("💡 SQL Schema Design Assistant")

# Generate dynamic table schema input box
table_definitions = get_all_create_table_statements(host, user, password, database)

# user input SQL/DDL statement
st.subheader("📋 Please input your requirements for the SQL query")
user_sql = st.text_area("Requirements for the SQL query:", height=100)

# Generate button
if st.button("🚀 Submit for LLM analysis")：
  # Combine input info
  input_data = {
    "Schema": table_definitions,
    "SQL/DDL statement": user_sql
  }

  # Send to OpenAI for analysis
  response = get_completion(table_definitions, user_sql)

  # Illustrate respone from LLM
  st.subheader("📢 Analysis from AI")
  st.success(resposne)
