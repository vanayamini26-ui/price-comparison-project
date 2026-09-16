import pandas as pd
import os

data_folder = "data"

files = os.listdir(data_folder)

print("\nFiles inside data folder:")
for file in files:
    print("-", file)

for file in files:
    if file.lower().endswith(".csv"):
        path = os.path.join(data_folder, file)

        df = pd.read_csv(path)

        print("\n" + "=" * 50)
        print("FILE:", file)
        print("ROWS:", len(df))
        print("COLUMNS:", len(df.columns))

        print("\nColumn names:")
        for column in df.columns:
            print("-", column)

        print("\nFirst 3 rows:")
        print(df.head(3))