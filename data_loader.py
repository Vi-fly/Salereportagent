import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv
import csv
from typing import List, Dict

load_dotenv()

def load_customer_data_csv(file_path: str) -> pd.DataFrame:
    """
    Load customer data from CSV file with proper handling of comma-separated values
    """
    try:
        # First, read with csv module to handle quoted fields properly
        rows = []
        with open(file_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            header = next(csv_reader)
            
            # Read all data rows
            for row in csv_reader:
                if len(row) > 0:  # Skip empty rows
                    rows.append(row)
        
        # Check if we have column mismatch
        if len(rows) > 0 and len(rows[0]) != len(header):
            print(f"⚠️ Column mismatch: Header has {len(header)} columns, data has {len(rows[0])} columns")
            # Create extended header with generic names for extra columns
            extended_header = header.copy()
            for i in range(len(header), len(rows[0])):
                extended_header.append(f'Extra_Column_{i}')
            header = extended_header
        
        # Create DataFrame from parsed data
        df = pd.DataFrame(rows, columns=header)
        
        # Clean up column names
        df.columns = df.columns.str.strip()
        
        # Ensure Customer_ID is treated as string
        df['Customer_ID'] = df['Customer_ID'].astype(str).str.strip()
        
        print(f"✅ Loaded {len(df)} records with {len(df.columns)} columns")
        print(f"📊 Customer IDs found: {sorted(df['Customer_ID'].unique())}")
        
        return df
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        raise

# Bonus: PostgreSQL loader
def load_customer_data_postgres():
    conn = psycopg2.connect(
        dbname=os.getenv('PG_DB'),
        user=os.getenv('PG_USER'),
        password=os.getenv('PG_PASSWORD'),
        host=os.getenv('PG_HOST'),
        port=os.getenv('PG_PORT', 5432)
    )
    query = "SELECT * FROM customer_data;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df 