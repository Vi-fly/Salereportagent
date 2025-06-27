#!/usr/bin/env python3
"""
Debug script to examine CSV structure
"""

import csv
import pandas as pd

print("=== CSV Debug Analysis ===")

# Method 1: Using csv module
print("\n1. Using csv module:")
with open('customer_data.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f"Header ({len(header)} columns): {header}")
    
    row1 = next(reader)
    print(f"Row 1 ({len(row1)} columns): {row1}")
    
    row2 = next(reader)
    print(f"Row 2 ({len(row2)} columns): {row2}")

# Method 2: Using pandas with different parameters
print("\n2. Using pandas with different parameters:")
try:
    df = pd.read_csv('customer_data.csv', engine='python')
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Customer_ID unique values: {df['Customer_ID'].unique()}")
    print(f"First row Customer_ID: {df.iloc[0]['Customer_ID']}")
    print(f"First row Product: {df.iloc[0]['Product']}")
except Exception as e:
    print(f"Error: {e}")

# Method 3: Manual parsing
print("\n3. Manual parsing:")
with open('customer_data.csv', 'r') as f:
    lines = f.readlines()
    print(f"Total lines: {len(lines)}")
    print(f"Line 1: {lines[0].strip()}")
    print(f"Line 2: {lines[1].strip()}")
    print(f"Line 3: {lines[2].strip()}") 