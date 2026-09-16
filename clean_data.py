import pandas as pd
import os

# ==============================
# Folder paths
# ==============================

AMAZON_FILE = "data/amazon_ll_electronic_products.csv/amazon_all_electronics_data.csv"

FLIPKART_EARPHONES = "data/flipkart.csv/flipkart_earphones.csv"
FLIPKART_LAPTOPS = "data/flipkart.csv/flipkart_laptops.csv"
FLIPKART_MOBILES = "data/flipkart.csv/flipkart_mobile_data.csv"

OUTPUT_FOLDER = "processed_data"

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("Loading datasets...")

# ==============================
# Load Amazon
# ==============================

amazon = pd.read_csv(AMAZON_FILE)

print("Amazon loaded:", len(amazon), "products")

# ==============================
# Load Flipkart datasets
# ==============================

flipkart_earphones = pd.read_csv(FLIPKART_EARPHONES)
flipkart_laptops = pd.read_csv(FLIPKART_LAPTOPS)
flipkart_mobiles = pd.read_csv(FLIPKART_MOBILES)

print("Flipkart earphones loaded:", len(flipkart_earphones))
print("Flipkart laptops loaded:", len(flipkart_laptops))
print("Flipkart mobiles loaded:", len(flipkart_mobiles))
print("\n" + "=" * 60)
print("AMAZON COLUMNS")
print(amazon.columns.tolist())

print("\n" + "=" * 60)
print("FLIPKART EARPHONES COLUMNS")
print(flipkart_earphones.columns.tolist())

print("\n" + "=" * 60)
print("FLIPKART LAPTOPS COLUMNS")
print(flipkart_laptops.columns.tolist())

print("\n" + "=" * 60)
print("FLIPKART MOBILES COLUMNS")
print(flipkart_mobiles.columns.tolist())
# ============================================================
# Clean Amazon dataset
# ============================================================

amazon_clean = amazon.copy()

amazon_clean = amazon_clean.rename(columns={
    "Product_Name": "product_name",
    "Price": "price",
    "Rating": "rating",
    "Review_Count": "review_count",
    "Product_URL": "product_url"
})

amazon_clean["source"] = "Amazon"
amazon_clean["category"] = "Electronics"

amazon_clean["price"] = pd.to_numeric(
    amazon_clean["price"],
    errors="coerce"
)

amazon_clean["rating"] = pd.to_numeric(
    amazon_clean["rating"],
    errors="coerce"
)

amazon_clean["review_count"] = pd.to_numeric(
    amazon_clean["review_count"],
    errors="coerce"
)

amazon_clean["product_name"] = (
    amazon_clean["product_name"]
    .astype(str)
    .str.strip()
)

print("\nAmazon cleaning completed.")
print("Amazon rows:", len(amazon_clean))
# ============================================================
# Clean Flipkart Earphones
# ============================================================

earphones_clean = flipkart_earphones.copy()

earphones_clean = earphones_clean.rename(columns={
    "Title": "product_name",
    "Product URL": "product_url",
    "Image URL": "image_url",
    "Rating": "rating",
    "Rating Count": "review_count",
    "Price": "price"
})

earphones_clean["source"] = "Flipkart"
earphones_clean["category"] = "Earphones"

# Clean price
earphones_clean["price"] = (
    earphones_clean["price"]
    .astype(str)
    .str.replace(r"[^\d.]", "", regex=True)
)

earphones_clean["price"] = pd.to_numeric(
    earphones_clean["price"],
    errors="coerce"
)

# Clean rating
earphones_clean["rating"] = pd.to_numeric(
    earphones_clean["rating"],
    errors="coerce"
)

# Clean review count
earphones_clean["review_count"] = (
    earphones_clean["review_count"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.extract(r"(\d+)", expand=False)
)

earphones_clean["review_count"] = pd.to_numeric(
    earphones_clean["review_count"],
    errors="coerce"
)

# Clean product name
earphones_clean["product_name"] = (
    earphones_clean["product_name"]
    .astype(str)
    .str.strip()
)

# Fix duplicated Flipkart URL
earphones_clean["product_url"] = (
    earphones_clean["product_url"]
    .astype(str)
    .str.replace(
        "https://www.flipkart.comhttps://www.flipkart.com",
        "https://www.flipkart.com",
        regex=False
    )
)

print("Flipkart earphones cleaning completed.")
print("Earphones rows:", len(earphones_clean))
# ============================================================
# Clean Flipkart Laptops
# ============================================================

laptops_clean = flipkart_laptops.copy()

laptops_clean = laptops_clean.rename(columns={
    "Title": "product_name",
    "Product Link": "product_url",
    "Image URL": "image_url",
    "Rating": "rating",
    "Ratings & Reviews": "review_info",
    "Price": "price"
})

laptops_clean["source"] = "Flipkart"
laptops_clean["category"] = "Laptops"

# Clean price
laptops_clean["price"] = (
    laptops_clean["price"]
    .astype(str)
    .str.replace(r"[^\d.]", "", regex=True)
)

laptops_clean["price"] = pd.to_numeric(
    laptops_clean["price"],
    errors="coerce"
)

# Clean rating
laptops_clean["rating"] = pd.to_numeric(
    laptops_clean["rating"],
    errors="coerce"
)

# Extract review count from values such as:
# "346 Ratings & 33 Reviews"
laptops_clean["review_count"] = (
    laptops_clean["review_info"]
    .astype(str)
    .str.extract(r"([\d,]+)\s+Reviews?", expand=False)
    .str.replace(",", "", regex=False)
)

laptops_clean["review_count"] = pd.to_numeric(
    laptops_clean["review_count"],
    errors="coerce"
)

# Clean product name
laptops_clean["product_name"] = (
    laptops_clean["product_name"]
    .astype(str)
    .str.strip()
)

print("Flipkart laptops cleaning completed.")
print("Laptop rows:", len(laptops_clean))
# ============================================================
# Clean Flipkart Mobiles
# ============================================================

mobiles_clean = flipkart_mobiles.copy()

mobiles_clean = mobiles_clean.rename(columns={
    "Title": "product_name",
    "Product Link": "product_url",
    "Image URL": "image_url",
    "Rating": "rating",
    "Ratings & Reviews": "review_info",
    "Price": "price"
})

mobiles_clean["source"] = "Flipkart"
mobiles_clean["category"] = "Mobiles"

# Clean price
mobiles_clean["price"] = (
    mobiles_clean["price"]
    .astype(str)
    .str.replace(r"[^\d.]", "", regex=True)
)

mobiles_clean["price"] = pd.to_numeric(
    mobiles_clean["price"],
    errors="coerce"
)

# Clean rating
mobiles_clean["rating"] = pd.to_numeric(
    mobiles_clean["rating"],
    errors="coerce"
)

# Extract review count
mobiles_clean["review_count"] = (
    mobiles_clean["review_info"]
    .astype(str)
    .str.extract(r"([\d,]+)\s+Reviews?", expand=False)
    .str.replace(",", "", regex=False)
)

mobiles_clean["review_count"] = pd.to_numeric(
    mobiles_clean["review_count"],
    errors="coerce"
)

# Clean product name
mobiles_clean["product_name"] = (
    mobiles_clean["product_name"]
    .astype(str)
    .str.strip()
)

print("Flipkart mobiles cleaning completed.")
print("Mobile rows:", len(mobiles_clean))
# ============================================================
# Combine Flipkart datasets
# ============================================================

flipkart_clean = pd.concat(
    [
        earphones_clean,
        laptops_clean,
        mobiles_clean
    ],
    ignore_index=True
)

print("\n" + "=" * 60)
print("FLIPKART DATASETS COMBINED")
print("Total Flipkart products:", len(flipkart_clean))

print("\nProducts by category:")
print(flipkart_clean["category"].value_counts())
# ============================================================
# Save cleaned datasets
# ============================================================

amazon_clean.to_csv(
    os.path.join(OUTPUT_FOLDER, "amazon_clean.csv"),
    index=False
)

flipkart_clean.to_csv(
    os.path.join(OUTPUT_FOLDER, "flipkart_clean.csv"),
    index=False
)

print("\n" + "=" * 60)
print("CLEANED DATASETS SAVED SUCCESSFULLY!")
print("Amazon:", os.path.join(OUTPUT_FOLDER, "amazon_clean.csv"))
print("Flipkart:", os.path.join(OUTPUT_FOLDER, "flipkart_clean.csv"))
# ============================================================
# Create final standardized datasets
# ============================================================

FINAL_COLUMNS = [
    "product_name",
    "price",
    "rating",
    "review_count",
    "product_url",
    "image_url",
    "category",
    "source"
]

# Amazon does not have image_url, so create it
if "image_url" not in amazon_clean.columns:
    amazon_clean["image_url"] = ""

amazon_final = amazon_clean[FINAL_COLUMNS].copy()
flipkart_final = flipkart_clean[FINAL_COLUMNS].copy()

# Remove products where price is unavailable
amazon_final = amazon_final.dropna(subset=["price"])
flipkart_final = flipkart_final.dropna(subset=["price"])

# Remove duplicate products
amazon_final = amazon_final.drop_duplicates(
    subset=["product_name", "price"]
)

flipkart_final = flipkart_final.drop_duplicates(
    subset=["product_name", "price"]
)

# Save final datasets
amazon_final.to_csv(
    os.path.join(OUTPUT_FOLDER, "amazon_final.csv"),
    index=False
)

flipkart_final.to_csv(
    os.path.join(OUTPUT_FOLDER, "flipkart_final.csv"),
    index=False
)

print("\n" + "=" * 60)
print("FINAL DATASETS CREATED")
print("Amazon final products:", len(amazon_final))
print("Flipkart final products:", len(flipkart_final))
print("Total final products:", len(amazon_final) + len(flipkart_final))
