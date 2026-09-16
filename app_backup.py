from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os

# ============================================================
# Flask Configuration
# ============================================================

app = Flask(__name__)
CORS(app)

# ============================================================
# Load Price Comparison Data
# ============================================================

DATA_FILE = os.path.join(
    "processed_data",
    "price_comparison.csv"
)

try:
    data = pd.read_csv(DATA_FILE)
    print("Price comparison data loaded successfully.")
    print("Total products:", len(data))

except FileNotFoundError:
    print("ERROR: price_comparison.csv not found.")
    data = pd.DataFrame()


# ============================================================
# Home Route
# ============================================================

@app.route("/")
def home():
    return jsonify({
        "message": "Smart Price Comparison API is running",
        "status": "success"
    })


# ============================================================
# Get All Products
# ============================================================

@app.route("/api/products", methods=["GET"])
def get_products():

    if data.empty:
        return jsonify({
            "error": "No product data available"
        }), 404

    products = data.fillna("").to_dict(orient="records")

    return jsonify(products)


# ============================================================
# Search Products
# ============================================================

@app.route("/api/search", methods=["GET"])
def search_products():

    if data.empty:
        return jsonify({
            "error": "No product data available"
        }), 404

    query = request.args.get("q", "").strip().lower()

    if not query:
        return jsonify([])

    result = data[
        data["amazon_product"]
        .astype(str)
        .str.lower()
        .str.contains(query, na=False)
    ]

    # Also search Flipkart product names
    flipkart_result = data[
        data["flipkart_product"]
        .astype(str)
        .str.lower()
        .str.contains(query, na=False)
    ]

    result = pd.concat(
        [result, flipkart_result]
    ).drop_duplicates()

    return jsonify(
        result.fillna("").to_dict(orient="records")
    )


# ============================================================
# Get Products by Category
# ============================================================

@app.route("/api/category/<category>", methods=["GET"])
def get_category(category):

    if data.empty:
        return jsonify({
            "error": "No product data available"
        }), 404

    result = data[
        data["category"]
        .astype(str)
        .str.lower() == category.lower()
    ]

    return jsonify(
        result.fillna("").to_dict(orient="records")
    )


# ============================================================
# Get Summary
# ============================================================

@app.route("/api/summary", methods=["GET"])
def get_summary():

    if data.empty:
        return jsonify({
            "error": "No product data available"
        }), 404

    amazon_cheaper = int(
        (data["cheaper_platform"] == "Amazon").sum()
    )

    flipkart_cheaper = int(
        (data["cheaper_platform"] == "Flipkart").sum()
    )

    same_price = int(
        (
            data["cheaper_platform"]
            .astype(str)
            .str.lower()
            == "same"
        ).sum()
    )

    return jsonify({
        "total_products": len(data),
        "amazon_cheaper": amazon_cheaper,
        "flipkart_cheaper": flipkart_cheaper,
        "same_price": same_price,
        "average_savings": round(
            float(data["savings"].mean()), 2
        ),
        "maximum_savings": round(
            float(data["savings"].max()), 2
        )
    })


# ============================================================
# Get Single Product
# ============================================================

@app.route("/api/product/<int:index>", methods=["GET"])
def get_product(index):

    if data.empty:
        return jsonify({
            "error": "No product data available"
        }), 404

    if index < 0 or index >= len(data):
        return jsonify({
            "error": "Product not found"
        }), 404

    product = data.iloc[index]

    return jsonify(
        product.fillna("").to_dict()
    )


# ============================================================
# Run Flask Server
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("SMART PRICE COMPARISON SYSTEM")
    print("=" * 60)
    print("Server starting...")
    print("Open: http://127.0.0.1:5000")
    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )