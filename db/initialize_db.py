import pandas as pd
import sqlite3
from dotenv import load_dotenv
import os

# Get .env value of PSGC_VERSION
# Load environment variables from .env file
load_dotenv()

# Get PSGC_VERSION from .env file
psgc_version = os.getenv('PSGC_VERSION')


# Path to the Excel file
excel_file_path = f"psgc_{psgc_version}.xlsx"

# Load the Excel file and sheet 'PSGC'
df = pd.read_excel(excel_file_path, sheet_name='PSGC')

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(f"psgc_{psgc_version}.db")
cursor = conn.cursor()

# Create a table for PSGC data (adjust column names and types as needed)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS PSGC (
        code TEXT PRIMARY KEY,
        name TEXT,
        correspondence_code TEXT,
        geographic_level TEXT,
        old_names TEXT,
        city_class TEXT,
        income_classification TEXT,
        urban_rural TEXT,
        status TEXT
    )
''')

# Insert data into the table
for index, row in df.iterrows():
    if pd.isna(row['10-digit PSGC']):
        print("skipping: " + row['Name'] + ". No PSGC Code registered")
        continue
    cursor.execute('''
        INSERT OR REPLACE INTO PSGC (
            code, name, correspondence_code, geographic_level, old_names, city_class,
            income_classification, urban_rural, status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        str(int(float(row['10-digit PSGC']))).rjust(10, "0"), 
        row['Name'], 
        row['Correspondence Code'], 
        row['Geographic Level'], 
        row['Old names'], 
        row['City Class'], 
        row['Income Classification'], 
        row['Urban / Rural'], 
        row['Status']
    ))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Data successfully loaded into SQLite database!")