import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Read Snowflake credentials from environment
sf_user = os.getenv('SNOWFLAKE_USER')
sf_password = os.getenv('SNOWFLAKE_PASSWORD')
sf_account = os.getenv('SNOWFLAKE_ACCOUNT')
sf_warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
sf_database = os.getenv('SNOWFLAKE_DATABASE')
sf_schema = os.getenv('SNOWFLAKE_SCHEMA')

# Load the CSV file
df = pd.read_csv(r'C:\Users\user\Documents\Pizza-Sales-Project\data\full_pizza_orders_flat.csv')

# Convert 'order_date' and 'order_time' to string format
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce').dt.date.astype(str)
df['order_time'] = pd.to_datetime(df['order_time'], errors='coerce').dt.time.astype(str)

# Verify the changes
print(df[['order_date', 'order_time']].head())

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=sf_user,
    password=sf_password,
    account=sf_account,
    warehouse=sf_warehouse,
    database=sf_database,
    schema=sf_schema
)
cs = conn.cursor()

# Create table (optional)
cs.execute("""
CREATE TABLE IF NOT EXISTS pizza_orders (
    order_id INT PRIMARY KEY,
    pizza_id VARCHAR,
    quantity INT,
    order_date DATE,
    order_time TIME,
    pizza_type_id VARCHAR,
    pizza_size VARCHAR(255),
    price DECIMAL(10, 2),
    name VARCHAR(255),
    category VARCHAR(255),
    ingredients TEXT
)
""")

# Insert each row into the table
for i, row in df.iterrows():
    # Convert row values to the appropriate types
    row_values = (
        int(row['order_id']),               # order_id as INT
        str(row['pizza_id']),               # pizza_id as VARCHAR
        int(row['quantity']),               # quantity as INT
        str(row['order_date']),             # order_date as string (YYYY-MM-DD)
        str(row['order_time']),             # order_time as string (HH:MM:SS)
        str(row['pizza_type_id']),          # pizza_type_id as VARCHAR
        str(row['pizza_size']),             # pizza_size as VARCHAR
        float(row['price']),                # price as DECIMAL
        str(row['name']),                   # name as VARCHAR
        str(row['category']),               # category as VARCHAR
        str(row['ingredients'])             # ingredients as TEXT
    )

    # Execute the insert query
    try:
        cs.execute("""
            INSERT INTO pizza_orders (
                order_id, pizza_id, quantity, order_date, order_time,
                pizza_type_id, pizza_size, price, name, category, ingredients
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, row_values)
    except Exception as e:
        print(f"❌ Failed on row {i}: {e}")
        print(f"Row {i} values: {row_values}")

# Commit the transaction and close connection
conn.commit()
cs.close()
conn.close()

print("✅ Data has been successfully pushed to Snowflake.")
