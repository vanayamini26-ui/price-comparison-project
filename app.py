from flask import Flask, jsonify, request,render_template
from flask_cors import CORS
import sqlite3
import os

# ============================================================
# Flask Configuration
# ============================================================

app = Flask(__name__)
CORS(app)

DB_FILE = "processed_data/price_comparison.db"


# ============================================================
# Database Connection
# ============================================================

def get_db_connection():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


# ============================================================
# Home / API Status
# ============================================================
@app.route("/")
def home():
    return render_template("index.html")



# ============================================================
# Get All Products
# ============================================================

@app.route("/api/products", methods=["GET"])
def get_products():

    connection = get_db_connection()

    products = connection.execute(
        "SELECT * FROM products"
    ).fetchall()

    connection.close()

    result = [dict(product) for product in products]

    return jsonify({
        "status": "success",
        "count": len(result),
        "products": result
    })


# ============================================================
# Get Single Product
# ============================================================

@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):

    connection = get_db_connection()

    product = connection.execute(
        "SELECT rowid AS id, * FROM products WHERE rowid = ?",
        (product_id,)
    ).fetchone()

    connection.close()

    if product is None:
        return jsonify({
            "status": "error",
            "message": "Product not found"
        }), 404

    return jsonify({
        "status": "success",
        "product": dict(product)
    })


# ============================================================
# Search Products
# ============================================================

@app.route("/api/search", methods=["GET"])
def search_products():

    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "status": "error",
            "message": "Please provide a search query"
        }), 400

    connection = get_db_connection()

    products = connection.execute(
        """
        SELECT rowid AS id, *
        FROM products
        WHERE amazon_product LIKE ?
           OR flipkart_product LIKE ?
        """,
        (f"%{query}%", f"%{query}%")
    ).fetchall()

    connection.close()

    result = [dict(product) for product in products]

    return jsonify({
        "status": "success",
        "count": len(result),
        "products": result
    })


# ============================================================
# Filter by Category
# ============================================================

@app.route("/api/category/<category_name>", methods=["GET"])
def get_category(category_name):

    connection = get_db_connection()

    products = connection.execute(
        """
        SELECT rowid AS id, *
        FROM products
        WHERE category = ?
        """,
        (category_name,)
    ).fetchall()

    connection.close()

    result = [dict(product) for product in products]

    return jsonify({
        "status": "success",
        "category": category_name,
        "count": len(result),
        "products": result
    })


# ============================================================
# Price Statistics
# ============================================================

@app.route("/api/statistics", methods=["GET"])
def statistics():

    connection = get_db_connection()

    total = connection.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    amazon_cheaper = connection.execute(
        """
        SELECT COUNT(*)
        FROM products
        WHERE cheaper_platform = 'Amazon'
        """
    ).fetchone()[0]

    flipkart_cheaper = connection.execute(
        """
        SELECT COUNT(*)
        FROM products
        WHERE cheaper_platform = 'Flipkart'
        """
    ).fetchone()[0]

    same_price = connection.execute(
        """
        SELECT COUNT(*)
        FROM products
        WHERE cheaper_platform NOT IN ('Amazon', 'Flipkart')
           OR cheaper_platform IS NULL
        """
    ).fetchone()[0]

    connection.close()

    return jsonify({
        "status": "success",
        "total_products": total,
        "amazon_cheaper": amazon_cheaper,
        "flipkart_cheaper": flipkart_cheaper,
        "same_price": same_price
    })


# ============================================================
# Start Server
# ============================================================

if __name__ == "__main__":

    if not os.path.exists(DB_FILE):
        print("ERROR: Database file not found!")
        print("Run: python database.py")
    else:

        print("=" * 60)
        print("SMART PRICE COMPARISON SYSTEM")
        print("=" * 60)

        print("Database connected successfully.")
        print("Database:", DB_FILE)

        print("\nServer starting...")
        print("Open: http://127.0.0.1:5000")
        print("=" * 60)

        app.run(
            host="127.0.0.1",
            port=5000,
            debug=True
        )