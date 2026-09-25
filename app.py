from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)

CORS(app)

DB_FILE = "processed_data/price_comparison.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db_connection():

    connection = sqlite3.connect(DB_FILE)

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# PAGE 1 - WELCOME
# ============================================================

@app.route("/")
def home():

    return send_from_directory(
        "welcome",
        "welcome.html"
    )


@app.route("/welcome/<path:filename>")
def welcome_files(filename):

    return send_from_directory(
        "welcome",
        filename
    )


# ============================================================
# PAGE 2 - LOGIN / SIGN UP
# ============================================================

@app.route("/login")
def login_page():

    return send_from_directory(
        "login",
        "login.html"
    )


@app.route("/login/<path:filename>")
def login_files(filename):

    return send_from_directory(
        "login",
        filename
    )


# ============================================================
# PAGE 3 - PRICEWISE HOME
# ============================================================

@app.route("/products")
def products_page():

    return render_template(
        "index.html"
    )


# ============================================================
# PAGE 4 - CATEGORY PRODUCTS
# ============================================================

@app.route("/category/<category_name>")
def category_page(category_name):

    category_map = {

        "all": "All",

        "mobiles": "Mobiles",

        "laptops": "Laptops",

        "earphones": "Earphones"

    }

    category_key = category_name.lower()

    if category_key not in category_map:

        return "Category not found", 404

    category = category_map[category_key]

    return render_template(
        "category.html",
        category=category
    )


# ============================================================
# PAGE 5 - PRODUCT COMPARISON
# ============================================================

@app.route("/product/<int:product_id>")
def product_page(product_id):

    return render_template(
        "product.html",
        product_id=product_id
    )


# ============================================================
# API - ALL PRODUCTS
# ============================================================

@app.route("/api/products", methods=["GET"])
def get_products():

    connection = get_db_connection()

    products = connection.execute(
        """
        SELECT rowid AS id, *
        FROM products
        """
    ).fetchall()

    connection.close()

    result = [
        dict(product)
        for product in products
    ]

    return jsonify({
        "status": "success",
        "count": len(result),
        "products": result
    })


# ============================================================
# API - SINGLE PRODUCT
# ============================================================

@app.route(
    "/api/products/<int:product_id>",
    methods=["GET"]
)
def get_product(product_id):

    connection = get_db_connection()

    product = connection.execute(
        """
        SELECT rowid AS id, *
        FROM products
        WHERE rowid = ?
        """,
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
# API - SEARCH
# ============================================================

@app.route("/api/search", methods=["GET"])
def search_products():

    query = request.args.get(
        "q",
        ""
    ).strip()

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
        (
            f"%{query}%",

            f"%{query}%"
        )
    ).fetchall()

    connection.close()

    result = [
        dict(product)
        for product in products
    ]

    return jsonify({

        "status": "success",

        "count": len(result),

        "products": result

    })


# ============================================================
# API - CATEGORY
# ============================================================

@app.route(
    "/api/category/<category_name>",
    methods=["GET"]
)
def get_category(category_name):

    category_map = {

        "mobiles": "Mobiles",

        "laptops": "Laptops",

        "earphones": "Earphones"

    }

    category_key = category_name.lower()

    if category_key not in category_map:

        return jsonify({

            "status": "error",

            "message": "Invalid category"

        }), 404

    category = category_map[category_key]

    connection = get_db_connection()

    products = connection.execute(
        """
        SELECT rowid AS id, *
        FROM products
        WHERE category = ?
        """,
        (category,)
    ).fetchall()

    connection.close()

    result = [
        dict(product)
        for product in products
    ]

    return jsonify({

        "status": "success",

        "category": category,

        "count": len(result),

        "products": result

    })


# ============================================================
# API - STATISTICS
# ============================================================

@app.route(
    "/api/statistics",
    methods=["GET"]
)
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
        WHERE cheaper_platform NOT IN
              ('Amazon', 'Flipkart')
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
# START SERVER
# ============================================================

if __name__ == "__main__":

    if not os.path.exists(DB_FILE):

        print("ERROR: Database file not found!")

        print(
            "Run: python database.py"
        )

    else:

        print("=" * 60)

        print(
            "PRICEWISE - PRICE COMPARISON SYSTEM"
        )

        print("=" * 60)

        print(
            "Database connected successfully."
        )

        print(
            "Database:",
            DB_FILE
        )

        print()

        print(
            "Welcome:"
        )

        print(
            "http://127.0.0.1:5000"
        )

        print()

        print(
            "Login:"
        )

        print(
            "http://127.0.0.1:5000/login"
        )

        print()

        print(
            "Products:"
        )

        print(
            "http://127.0.0.1:5000/products"
        )

        print()

        print(
            "Category:"
        )

        print(
            "http://127.0.0.1:5000/category/Mobiles"
        )

        print()

        print(
            "Product Comparison:"
        )

        print(
            "http://127.0.0.1:5000/product/1"
        )

        print()

        print(
            "Phone URL:"
        )

        print(
            "http://10.14.11.218:5000"
        )

        print()

        print(
            "Server starting..."
        )

        print("=" * 60)

        app.run(
            host="0.0.0.0",
            port=5000,
            debug=True
        )