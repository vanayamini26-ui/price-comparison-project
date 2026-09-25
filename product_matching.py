import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# Configuration
# ============================================================

AMAZON_FILE = "processed_data/amazon_final.csv"
FLIPKART_FILE = "processed_data/flipkart_final.csv"

OUTPUT_FILE = "processed_data/final_product_matches.csv"

SIMILARITY_THRESHOLD = 0.20


# ============================================================
# Load datasets
# ============================================================

print("Loading datasets...")

amazon = pd.read_csv(AMAZON_FILE)
flipkart = pd.read_csv(FLIPKART_FILE)

print("Amazon products:", len(amazon))
print("Flipkart products:", len(flipkart))

print("\nAmazon columns:")
print(amazon.columns.tolist())

print("\nFlipkart columns:")
print(flipkart.columns.tolist())


# ============================================================
# Detect Amazon product category
# ============================================================

def detect_category(name):

    name = str(name).lower()

    earphone_keywords = [
        "earphone",
        "earphones",
        "headphone",
        "headphones",
        "earbud",
        "earbuds",
        "airpods",
        "neckband",
        "tws"
    ]

    laptop_keywords = [
        "laptop",
        "notebook",
        "chromebook",
        "macbook"
    ]

    mobile_keywords = [
        "iphone",
        "smartphone",
        "mobile phone",
        "galaxy",
        "redmi",
        "realme",
        "oneplus",
        "pixel",
        "poco",
        "vivo",
        "oppo",
        "motorola",
        "nothing phone"
    ]

    if any(word in name for word in earphone_keywords):
        return "Earphones"

    if any(word in name for word in laptop_keywords):
        return "Laptops"

    if any(word in name for word in mobile_keywords):
        return "Mobiles"

    return "Other"


# Amazon category detection
amazon["category"] = amazon["product_name"].apply(detect_category)


# Flipkart already has categories,
# but make sure missing categories are handled
flipkart["category"] = flipkart["category"].fillna("Other")


print("\nAmazon categories:")
print(amazon["category"].value_counts())

print("\nFlipkart categories:")
print(flipkart["category"].value_counts())


# ============================================================
# Clean product names
# ============================================================

def clean_product_name(name):

    name = str(name).lower()

    # Remove URLs
    name = re.sub(r"http\S+", " ", name)

    # Replace special characters with spaces
    name = re.sub(r"[^a-z0-9]+", " ", name)

    # Remove extra spaces
    name = re.sub(r"\s+", " ", name).strip()

    return name


amazon["clean_name"] = amazon["product_name"].apply(
    clean_product_name
)

flipkart["clean_name"] = flipkart["product_name"].apply(
    clean_product_name
)


print("\nExample cleaned product names:")

print("\nAmazon:")
print(
    amazon[
        ["product_name", "clean_name"]
    ].head(3).to_string(index=False)
)

print("\nFlipkart:")
print(
    flipkart[
        ["product_name", "clean_name"]
    ].head(3).to_string(index=False)
)


# ============================================================
# Extract important product tokens
# ============================================================

def get_tokens(name):

    return set(str(name).lower().split())


# ============================================================
# Extract brand
# ============================================================

BRANDS = [
    "apple",
    "samsung",
    "oneplus",
    "realme",
    "redmi",
    "xiaomi",
    "vivo",
    "oppo",
    "motorola",
    "google",
    "nothing",
    "poco",
    "hp",
    "dell",
    "acer",
    "asus",
    "lenovo",
    "msi",
    "portronics",
    "boat",
    "jbl",
    "sony",
    "noise",
    "ptron"
]


def get_brand(name):

    name = str(name).lower()

    for brand in BRANDS:

        if re.search(r"\b" + re.escape(brand) + r"\b", name):
            return brand

    return ""


amazon["brand"] = amazon["clean_name"].apply(get_brand)
flipkart["brand"] = flipkart["clean_name"].apply(get_brand)


# ============================================================
# Extract important specification tokens
# ============================================================

def get_specs(name):

    name = str(name).lower()

    specs = set()

    # RAM
    ram_matches = re.findall(
        r"\b\d+\s*gb\s*(?:ram)?\b",
        name
    )

    for item in ram_matches:
        specs.add(item.replace(" ", ""))

    # Storage
    storage_matches = re.findall(
        r"\b\d+\s*(?:gb|tb)\s*(?:storage|ssd|rom)?\b",
        name
    )

    for item in storage_matches:
        specs.add(item.replace(" ", ""))

    # Processor/model numbers
    model_matches = re.findall(
        r"\b(?:i3|i5|i7|i9|r3|r5|r7|r9|[a-z]+\d{2,}[a-z0-9-]*)\b",
        name
    )

    for item in model_matches:
        specs.add(item)

    return specs


amazon["specs"] = amazon["clean_name"].apply(get_specs)
flipkart["specs"] = flipkart["clean_name"].apply(get_specs)


# ============================================================
# TF-IDF Vectorization
# ============================================================

print("\nCreating TF-IDF vectors...")

all_names = pd.concat(
    [
        amazon["clean_name"],
        flipkart["clean_name"]
    ],
    ignore_index=True
)

vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    min_df=1,
    sublinear_tf=True
)

tfidf_matrix = vectorizer.fit_transform(all_names)

amazon_count = len(amazon)

amazon_vectors = tfidf_matrix[:amazon_count]

flipkart_vectors = tfidf_matrix[amazon_count:]

print("TF-IDF matrix created.")
print("Matrix shape:", tfidf_matrix.shape)
print("Amazon TF-IDF shape:", amazon_vectors.shape)
print("Flipkart TF-IDF shape:", flipkart_vectors.shape)


# ============================================================
# Product Matching
# ============================================================

print("\nStarting product matching...")

matches = []


for category in amazon["category"].unique():

    print("\nMatching category:", category)

    amazon_category = amazon[
        amazon["category"] == category
    ]

    flipkart_category = flipkart[
        flipkart["category"] == category
    ]

    if flipkart_category.empty:

        print(
            "No Flipkart products found for",
            category
        )

        continue

    amazon_indices = amazon_category.index.tolist()
    flipkart_indices = flipkart_category.index.tolist()

    # Calculate TF-IDF cosine similarity
    similarity_matrix = cosine_similarity(
        amazon_vectors[amazon_indices],
        flipkart_vectors[flipkart_indices]
    )

    # --------------------------------------------------------
    # Find best match for every Amazon product
    # --------------------------------------------------------

    for i, amazon_index in enumerate(amazon_indices):

        # Sort candidates by similarity
        candidate_positions = similarity_matrix[
            i
        ].argsort()[::-1]

        best_match_found = False

        for position in candidate_positions[:10]:

            flipkart_index = flipkart_indices[position]

            similarity_score = similarity_matrix[
                i,
                position
            ]

            amazon_brand = amazon.loc[
                amazon_index,
                "brand"
            ]

            flipkart_brand = flipkart.loc[
                flipkart_index,
                "brand"
            ]

            amazon_specs = amazon.loc[
                amazon_index,
                "specs"
            ]

            flipkart_specs = flipkart.loc[
                flipkart_index,
                "specs"
            ]

            # ------------------------------------------------
            # Brand check
            # ------------------------------------------------

            if (
                amazon_brand
                and flipkart_brand
                and amazon_brand != flipkart_brand
            ):
                continue

            # ------------------------------------------------
            # Specification check
            # ------------------------------------------------

            common_specs = (
                amazon_specs & flipkart_specs
            )

            # If both products have important specs,
            # require at least one common specification
            if (
                amazon_specs
                and flipkart_specs
                and len(common_specs) == 0
            ):
                continue

            # ------------------------------------------------
            # Similarity threshold
            # ------------------------------------------------

            if similarity_score < SIMILARITY_THRESHOLD:
                continue

            # ------------------------------------------------
            # Accept match
            # ------------------------------------------------

            matches.append({

                "amazon_index":
                    amazon_index,

                "flipkart_index":
                    flipkart_index,

                "amazon_product":
                    amazon.loc[
                        amazon_index,
                        "product_name"
                    ],

                "flipkart_product":
                    flipkart.loc[
                        flipkart_index,
                        "product_name"
                    ],

                "amazon_price":
                    amazon.loc[
                        amazon_index,
                        "price"
                    ],

                "flipkart_price":
                    flipkart.loc[
                        flipkart_index,
                        "price"
                    ],

                "amazon_rating":
                    amazon.loc[
                        amazon_index,
                        "rating"
                    ],

                "flipkart_rating":
                    flipkart.loc[
                        flipkart_index,
                        "rating"
                    ],

                "amazon_url":
                    amazon.loc[
                        amazon_index,
                        "product_url"
                    ],

                "flipkart_url":
                    flipkart.loc[
                        flipkart_index,
                        "product_url"
                    ],

                "amazon_image":
                    amazon.loc[
                        amazon_index,
                        "image_url"
                    ],

                "flipkart_image":
                    flipkart.loc[
                        flipkart_index,
                        "image_url"
                    ],

                "category":
                    category,

                "similarity_score":
                    round(
                        float(similarity_score),
                        4
                    ),

                "brand":
                    amazon_brand

            })

            best_match_found = True

            break


# ============================================================
# Matching completed
# ============================================================

print("\nProduct matching completed.")

print(
    "Total matches:",
    len(matches)
)


# ============================================================
# Save final matches
# ============================================================

if matches:

    matches_df = pd.DataFrame(matches)

    matches_df = matches_df.sort_values(
        by="similarity_score",
        ascending=False
    )

    matches_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        "\nFinal matches saved to:"
    )

    print(OUTPUT_FILE)


# ============================================================
# Inspect sample matches
# ============================================================

print("\n" + "=" * 70)

print("SAMPLE PRODUCT MATCHES")

print("=" * 70)


for _, match in pd.DataFrame(matches).head(10).iterrows():

    print("\nAmazon:")
    print(match["amazon_product"])

    print(
        "Amazon Price: ₹",
        match["amazon_price"]
    )

    print("\nFlipkart:")
    print(match["flipkart_product"])

    print(
        "Flipkart Price: ₹",
        match["flipkart_price"]
    )

    print(
        "Category:",
        match["category"]
    )

    print(
        "Similarity:",
        match["similarity_score"]
    )

    print(
        "-" * 70
    )


# ============================================================
# Similarity Score Analysis
# ============================================================

if matches:

    scores_series = pd.Series(
        [
            match["similarity_score"]
            for match in matches
        ]
    )

    print("\n" + "=" * 70)

    print("SIMILARITY SCORE ANALYSIS")

    print("=" * 70)

    print(
        "Minimum:",
        round(scores_series.min(), 4)
    )

    print(
        "Maximum:",
        round(scores_series.max(), 4)
    )

    print(
        "Mean:",
        round(scores_series.mean(), 4)
    )

    print(
        "Median:",
        round(scores_series.median(), 4)
    )

    print("\nScore distribution:")

    print(
        scores_series.describe(
            percentiles=[
                0.10,
                0.25,
                0.50,
                0.75,
                0.90,
                0.95
            ]
        )
    )

else:

    print(
        "\nNo valid product matches found."
    )