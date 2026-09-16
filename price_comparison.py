
import pandas as pd
import os

# ============================================================
# Configuration
# ============================================================

MATCHES_FILE = "processed_data/final_product_matches.csv"
OUTPUT_FILE = "processed_data/price_comparison.csv"


# ============================================================
# Load matched products
# ============================================================

print("Loading matched products...")

matches = pd.read_csv(MATCHES_FILE)

print("Total matched products:", len(matches))

print("\nColumns:")
print(matches.columns.tolist())


# ============================================================
# Check required columns
# ============================================================

required_columns = [
    "amazon_price",
    "flipkart_price"
]

for column in required_columns:
    if column not in matches.columns:
        raise ValueError(
            f"Required column '{column}' not found in CSV."
        )


# ============================================================
# Convert prices to numeric
# ============================================================

matches["amazon_price"] = pd.to_numeric(
    matches["amazon_price"],
    errors="coerce"
)

matches["flipkart_price"] = pd.to_numeric(
    matches["flipkart_price"],
    errors="coerce"
)


# ============================================================
# Remove products with missing prices
# ============================================================

matches = matches.dropna(
    subset=["amazon_price", "flipkart_price"]
).copy()


# ============================================================
# Calculate price difference
# ============================================================

matches["price_difference"] = (
    matches["amazon_price"] -
    matches["flipkart_price"]
)


# ============================================================
# Find cheaper platform
# ============================================================

def find_cheaper(row):

    if row["amazon_price"] < row["flipkart_price"]:
        return "Amazon"

    elif row["flipkart_price"] < row["amazon_price"]:
        return "Flipkart"

    else:
        return "Same Price"


matches["cheaper_platform"] = matches.apply(
    find_cheaper,
    axis=1
)


# ============================================================
# Calculate savings
# ============================================================

matches["savings"] = (
    matches["amazon_price"] -
    matches["flipkart_price"]
).abs()


# ============================================================
# Calculate percentage difference
# ============================================================

matches["price_difference_percentage"] = (
    matches["savings"] /
    matches[["amazon_price", "flipkart_price"]].min(axis=1)
) * 100


matches["price_difference_percentage"] = (
    matches["price_difference_percentage"].round(2)
)


# ============================================================
# Save price comparison
# ============================================================

os.makedirs(
    "processed_data",
    exist_ok=True
)

matches.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# Display results
# ============================================================

print("\nPrice comparison completed.")

print("\nFile saved to:")
print(OUTPUT_FILE)


print("\n" + "=" * 70)
print("PRICE COMPARISON RESULTS")
print("=" * 70)


display_columns = [
    "amazon_price",
    "flipkart_price",
    "price_difference",
    "cheaper_platform",
    "savings",
    "price_difference_percentage"
]


print(
    matches[display_columns]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 70)
print("PRICE COMPARISON SUMMARY")
print("=" * 70)

print(
    "\nAmazon cheaper:",
    (matches["cheaper_platform"] == "Amazon").sum()
)

print(
    "Flipkart cheaper:",
    (matches["cheaper_platform"] == "Flipkart").sum()
)

print(
    "Same price:",
    (matches["cheaper_platform"] == "Same Price").sum()
)

print(
    "\nAverage savings: ₹",
    round(matches["savings"].mean(), 2)
)

print(
    "Maximum savings: ₹",
    round(matches["savings"].max(), 2)
)
