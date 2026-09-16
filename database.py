import sqlite3
import pandas as pd
import os

# ============================================================
# Configuration
# ============================================================

CSV_FILE = "processed_data/price_comparison.csv"
DB_FILE = "processed_data/price_comparison.db"


# ============================================================
# Create Database
# ============================================================

def create_database():

    if not os.path.exists(CSV_FILE):
        print("ERROR: price_comparison.csv not found.")
        return

    print("Loading price comparison data...")

    df = pd.read_csv(CSV_FILE)

    print("Total records:", len(df))

    # Create processed_data folder if needed
    os.makedirs("processed_data", exist_ok=True)

    # Connect to SQLite database
    connection = sqlite3.connect(DB_FILE)

    # Store dataframe as table
    df.to_sql(
        "products",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()

    print("\nDatabase created successfully!")
    print("Database file:")
    print(DB_FILE)

    print("\nTable created: products")


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    create_database()