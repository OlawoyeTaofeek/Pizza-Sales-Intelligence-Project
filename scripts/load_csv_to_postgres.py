import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# === Read the CSV ===
merged_df = pd.read_csv("data/full_pizza_orders_flat.csv")

# === Connect to PostgreSQL ===
# Update these with your PostgreSQL credentials
host = "localhost"
port = "5433"
dbname = "your_dbname"
user = "your_username"
password = "your_password"

# Create the connection URL
conn_str = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
engine = create_engine(conn_str)

# === Create table if not exists ===
create_table_sql = """
CREATE TABLE IF NOT EXISTS pizza_orders (
    order_id INT PRIMARY KEY,
    pizza_id INT,
    quantity INT,
    order_date DATE,
    order_time TIME,
    pizza_type_id INT,
    pizza_size VARCHAR(255),
    price DECIMAL(10, 2)
    name VARCHAR(255),
    category VARCHAR(255),
    ingredients VARCHAR(255),
);
"""

# Create a connection to execute the SQL
with psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password) as conn:
    with conn.cursor() as cursor:
        cursor.execute(create_table_sql)
        conn.commit()

# === Push the data to PostgreSQL ===
merged_df.to_sql("pizza_orders", engine, if_exists="replace", index=False)

print("✅ Data has been successfully pushed to PostgreSQL.")
