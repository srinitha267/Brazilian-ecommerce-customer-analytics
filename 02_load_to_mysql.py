import os
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine

#Locate and read the cleaned dataset
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, 'cleaned_olist_customers.csv')

print(f"Reading dataset: {csv_path}")
df = pd.read_csv(csv_path)

#Database credentials
DB_USER = 'root'
DB_PASS = 'Mysql@123'   
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'olist_ecommerce'

#URL-encode the password safely (escapes the '@' symbol so MySQL connects cleanly)
safe_password = quote_plus(DB_PASS)
connection_string = f"mysql+pymysql://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

#Upload to MySQL
try:
    print(f"Connecting to MySQL database '{DB_NAME}'...")
    engine = create_engine(connection_string)
    
    print(f"Uploading {len(df):,} records into table 'customers'...")
    df.to_sql(
        name='customers',
        con=engine,
        if_exists='replace',   #Overwrites table with clean data
        index=False,
        chunksize=10000        #Fast batch loading
    )
    print("✅ Upload completed successfully!")
except Exception as e:
    print(f"❌ Error occurred: {e}")
