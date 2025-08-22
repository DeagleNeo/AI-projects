import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
#os.environ["http_proxy"] = "http://127.0.0.1:1083"
#os.environ["https_proxy"] = "http://127.0.0.1:1083"

client = OpenAI()

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

st.title("💡 SQL Schema Design Assistant")

# user input number of tables
num_tables = st.number_input("Please input the number of tables: ", min_value=1, max_value=10, step=1, value=1)

# Generate dynamic table schema input box
table_definitions = []
st.subheader("📝 Please input the table schema(SQL/DDL statement)")
for i in range(num_tables):
  table_def = st.text_area(f"Table {i+1} Schema(SQL/DDL statement): ", height=150)
  table_definitions.append(table_def)

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
