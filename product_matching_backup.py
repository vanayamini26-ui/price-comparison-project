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

SIMILARITY_THRESHOLD = 0.30


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
# Category Detection
# ============================================================

def detect_category(name):

    name = str(name).lower()

    earphone_keywords = [
        "earphone", "earphones",
        "headphone", "headphones",
        "earbud", "earbuds",
        "airpods", "neckband", "tws"
    ]

    laptop_keywords = [
        "laptop", "notebook",
        "chromebook", "macbook"
    ]

    mobile_keywords = [
        "iphone", "smartphone",
        "mobile phone", "galaxy",
        "redmi", "realme",
        "oneplus", "pixel",
        "poco", "vivo",
        "oppo", "motorola",
        "nothing phone"
    ]

    if any(word in name for word in earphone_keywords):
        return "Earphones"

    if any(word in name for word in laptop_keywords):
        return "Laptops"

    if any(word in name for word in mobile_keywords):
        return "Mobiles"

    return "Other"


amazon["category"] = amazon["product_name"].apply(
    detect_category
)

flipkart["category"] = flipkart["category"].fillna("Other")

print("\nAmazon categories:")
print(amazon["category"].value_counts())

print("\nFlipkart categories:")
print(flipkart["category"].value_counts())


# ============================================================
# Clean Product Names
# ============================================================

def clean_product_name(name):

    name = str(name).lower()

    name = re.sub(
        r"http\S+",
        " ",
        name
    )

    name = re.sub(
        r"[^a-z0-9]+",
        " ",
        name
    )

    name = re.sub(
        r"\s+",
        " ",
        name
    ).strip()

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
# Brand Extraction
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

        if re.search(
            r"\b" + re.escape(brand) + r"\b",
            name
        ):
            return brand

    return ""


amazon["brand"] = amazon["clean_name"].apply(
    get_brand
)

flipkart["brand"] = flipkart["clean_name"].apply(
    get_brand
)


# ============================================================
# Model Extraction
# ============================================================

def get_model(name):

    name = str(name).lower()

    # --------------------------------------------------------
    # Apple iPhones
    # --------------------------------------------------------

    match = re.search(
        r"\biphone\s+(\d+)(?:\s+(pro|max|plus|mini|promax))?",
        name
    )

    if match:

        number = match.group(1)
        variant = match.group(2)

        if variant:
            return "iphone " + number + " " + variant

        return "iphone " + number


    # --------------------------------------------------------
    # Samsung Galaxy
    # --------------------------------------------------------

    match = re.search(
        r"\bgalaxy\s+([a-z]?\d+(?:\s+(?:ultra|plus|fe|pro))?)",
        name
    )

    if match:
        return "galaxy " + match.group(1)


    # --------------------------------------------------------
    # OnePlus
    # --------------------------------------------------------

    match = re.search(
        r"\boneplus\s+([a-z0-9]+(?:\s+[a-z0-9]+){0,3})",
        name
    )

    if match:

        model = match.group(1)

        # Stop before specifications
        model = re.split(
            r"\b(?:5g|4g|gb|ram|storage|black|blue|green|silver|grey|gray)\b",
            model
        )[0].strip()

        return "oneplus " + model


    # --------------------------------------------------------
    # Realme
    # --------------------------------------------------------

    match = re.search(
        r"\brealme\s+([a-z0-9]+(?:\s+[a-z0-9]+){0,3})",
        name
    )

    if match:

        model = match.group(1)

        model = re.split(
            r"\b(?:5g|4g|gb|ram|storage|black|blue|green|purple)\b",
            model
        )[0].strip()

        return "realme " + model


    # --------------------------------------------------------
    # Redmi
    # --------------------------------------------------------

    match = re.search(
        r"\bredmi\s+([a-z0-9]+(?:\s+[a-z0-9]+){0,2})",
        name
    )

    if match:

        model = match.group(1)

        model = re.split(
            r"\b(?:5g|4g|gb|ram|storage|black|blue|green)\b",
            model
        )[0].strip()

        return "redmi " + model


    # --------------------------------------------------------
    # HP laptops
    # --------------------------------------------------------

    match = re.search(
        r"\bhp\s+([a-z0-9]+(?:\s+[a-z0-9]+){0,2})",
        name
    )

    if match:

        model = match.group(1)

        model = re.split(
            r"\b(?:intel|amd|ryzen|core|gb|ssd|windows|laptop)\b",
            model
        )[0].strip()

        return "hp " + model


    # --------------------------------------------------------
    # Dell laptops
    # --------------------------------------------------------

    match = re.search(
        r"\bdell\s+([a-z0-9]+(?:\s+[a-z0-9]+){0,2})",
        name
    )

    if match:

        model = match.group(1)

        model = re.split(
            r"\b(?:intel|amd|ryzen|core|gb|ssd|windows|laptop)\b",
            model
        )[0].strip()

        return "dell " + model


    # --------------------------------------------------------
    # Acer laptops
    # --------------------------------------------------------

    match = re.search(
        r"\bacer\s+([a-z0-9]+(?:\s+[a-z0-9]+){0,2})",
        name
    )

    if match:

        model = match.group(1)

        model = re.split(
            r"\b(?:intel|amd|ryzen|core|gb|ssd|windows|laptop)\b",
            model
        )[0].strip()

        return "acer " + model


    # --------------------------------------------------------
    # Generic fallback
    # --------------------------------------------------------

    words = name.split()

    if len(words) >= 2:

        return " ".join(words[:2])

    return name


amazon["model"] = amazon["clean_name"].apply(
    get_model
)

flipkart["model"] = flipkart["clean_name"].apply(
    get_model
)


# ============================================================
# Specification Extraction
# ============================================================

def get_storage(name):

    name = str(name).lower()

    matches = re.findall(
        r"\b(\d+)\s*(gb|tb)\b",
        name
    )

    values = []

    for number, unit in matches:

        values.append(
            number + unit
        )

    return set(values)


def get_ram(name):

    name = str(name).lower()

    matches = re.findall(
        r"\b(\d+)\s*gb\s*(?:ram)?\b",
        name
    )

    return set(matches)


amazon["storage"] = amazon["clean_name"].apply(
    get_storage
)

flipkart["storage"] = flipkart["clean_name"].apply(
    get_storage
)

amazon["ram"] = amazon["clean_name"].apply(
    get_ram
)

flipkart["ram"] = flipkart["clean_name"].apply(
    get_ram
)


# ============================================================
# TF-IDF
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

tfidf_matrix = vectorizer.fit_transform(
    all_names
)

amazon_count = len(amazon)

amazon_vectors = tfidf_matrix[:amazon_count]

flipkart_vectors = tfidf_matrix[amazon_count:]

print(
    "TF-IDF matrix created."
)

print(
    "Matrix shape:",
    tfidf_matrix.shape
)

print(
    "Amazon TF-IDF shape:",
    amazon_vectors.shape
)

print(
    "Flipkart TF-IDF shape:",
    flipkart_vectors.shape
)


# ============================================================
# Product Matching
# ============================================================

print("\nStarting product matching...")

matches = []


for category in amazon["category"].unique():

    print(
        "\nMatching category:",
        category
    )

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

    similarity_matrix = cosine_similarity(
        amazon_vectors[amazon_indices],
        flipkart_vectors[flipkart_indices]
    )


    # --------------------------------------------------------
    # Match each Amazon product
    # --------------------------------------------------------

    for i, amazon_index in enumerate(
        amazon_indices
    ):

        candidate_positions = similarity_matrix[
            i
        ].argsort()[::-1]

        best_match = None
        best_score = 0


        # Check top 20 candidates
        for position in candidate_positions[:20]:

            flipkart_index = flipkart_indices[
                position
            ]

            similarity_score = float(
                similarity_matrix[
                    i,
                    position
                ]
            )


            # ------------------------------------------------
            # Brand check
            # ------------------------------------------------

            amazon_brand = amazon.loc[
                amazon_index,
                "brand"
            ]

            flipkart_brand = flipkart.loc[
                flipkart_index,
                "brand"
            ]

            if (
                amazon_brand
                and flipkart_brand
                and amazon_brand != flipkart_brand
            ):
                continue


            # ------------------------------------------------
            # Model check
            # ------------------------------------------------

            amazon_model = amazon.loc[
                amazon_index,
                "model"
            ]

            flipkart_model = flipkart.loc[
                flipkart_index,
                "model"
            ]

            # Strong protection against
            # iPhone 15 vs iPhone 15 Plus
            if (
                category == "Mobiles"
                and amazon_model
                and flipkart_model
                and amazon_model != flipkart_model
            ):
                continue


            # ------------------------------------------------
            # Storage check
            # ------------------------------------------------

            amazon_storage = amazon.loc[
                amazon_index,
                "storage"
            ]

            flipkart_storage = flipkart.loc[
                flipkart_index,
                "storage"
            ]

            if (
                amazon_storage
                and flipkart_storage
                and amazon_storage.isdisjoint(
                    flipkart_storage
                )
            ):
                continue


            # ------------------------------------------------
            # RAM check
            # ------------------------------------------------

            amazon_ram = amazon.loc[
                amazon_index,
                "ram"
            ]

            flipkart_ram = flipkart.loc[
                flipkart_index,
                "ram"
            ]

            if (
                amazon_ram
                and flipkart_ram
                and amazon_ram.isdisjoint(
                    flipkart_ram
                )
            ):
                continue


            # ------------------------------------------------
            # Similarity threshold
            # ------------------------------------------------

            if similarity_score < SIMILARITY_THRESHOLD:
                continue


            # ------------------------------------------------
            # Best valid candidate
            # ------------------------------------------------

            if similarity_score > best_score:

                best_score = similarity_score

                best_match = flipkart_index


        # ----------------------------------------------------
        # Save valid match
        # ----------------------------------------------------

        if best_match is not None:

            matches.append({

                "amazon_index":
                    amazon_index,

                "flipkart_index":
                    best_match,

                "amazon_product":
                    amazon.loc[
                        amazon_index,
                        "product_name"
                    ],

                "flipkart_product":
                    flipkart.loc[
                        best_match,
                        "product_name"
                    ],

                "amazon_price":
                    amazon.loc[
                        amazon_index,
                        "price"
                    ],

                "flipkart_price":
                    flipkart.loc[
                        best_match,
                        "price"
                    ],

                "amazon_rating":
                    amazon.loc[
                        amazon_index,
                        "rating"
                    ],

                "flipkart_rating":
                    flipkart.loc[
                        best_match,
                        "rating"
                    ],

                "amazon_url":
                    amazon.loc[
                        amazon_index,
                        "product_url"
                    ],

                "flipkart_url":
                    flipkart.loc[
                        best_match,
                        "product_url"
                    ],

                "amazon_image":
                    amazon.loc[
                        amazon_index,
                        "image_url"
                    ],

                "flipkart_image":
                    flipkart.loc[
                        best_match,
                        "image_url"
                    ],

                "category":
                    category,

                "brand":
                    amazon.loc[
                        amazon_index,
                        "brand"
                    ],

                "model":
                    amazon.loc[
                        amazon_index,
                        "model"
                    ],

                "similarity_score":
                    round(
                        best_score,
                        4
                    )
            })


# ============================================================
# Save Results
# ============================================================

print(
    "\nProduct matching completed."
)

print(
    "Total matches:",
    len(matches)
)


if matches:

    matches_df = pd.DataFrame(
        matches
    )

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

    print(
        OUTPUT_FILE
    )


# ============================================================
# Sample Matches
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    "SAMPLE PRODUCT MATCHES"
)

print(
    "=" * 70
)


if matches:

    for match in matches[:10]:

        print("\nAmazon:")
        print(
            match["amazon_product"]
        )

        print(
            "Amazon Price: ₹",
            match["amazon_price"]
        )

        print("\nFlipkart:")
        print(
            match["flipkart_product"]
        )

        print(
            "Flipkart Price: ₹",
            match["flipkart_price"]
        )

        print(
            "Category:",
            match["category"]
        )

        print(
            "Model:",
            match["model"]
        )

        print(
            "Similarity:",
            match["similarity_score"]
        )

        print(
            "-" * 70
        )


# ============================================================
# Similarity Analysis
# ============================================================

if matches:

    scores = [
        match["similarity_score"]
        for match in matches
    ]

    scores_series = pd.Series(
        scores
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "SIMILARITY SCORE ANALYSIS"
    )

    print(
        "=" * 70
    )

    print(
        "Minimum:",
        round(
            scores_series.min(),
            4
        )
    )

    print(
        "Maximum:",
        round(
            scores_series.max(),
            4
        )
    )

    print(
        "Mean:",
        round(
            scores_series.mean(),
            4
        )
    )

    print(
        "Median:",
        round(
            scores_series.median(),
            4
        )
    )

    print(
        "\nScore distribution:"
    )

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