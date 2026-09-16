
// ============================================================
// Smart Price Comparison - Frontend JavaScript
// ============================================================

const API_BASE = "/api";


// ============================================================
// Page Load
// ============================================================

document.addEventListener("DOMContentLoaded", function () {
    loadProducts();
    loadStatistics();

    // Search when Enter key is pressed
    const searchInput = document.getElementById("searchInput");

    searchInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            searchProducts();
        }
    });
});


// ============================================================
// Load All Products
// ============================================================

async function loadProducts() {

    showLoading();

    try {

        const response = await fetch(`${API_BASE}/products`);

        if (!response.ok) {
            throw new Error("Failed to load products");
        }

        const data = await response.json();

        displayProducts(data.products);

        updateResultCount(data.count);

    } catch (error) {

        console.error("Error:", error);

        showError(
            "Unable to load products. Please make sure Flask server is running."
        );
    }
}


// ============================================================
// Search Products
// ============================================================

async function searchProducts() {

    const input = document.getElementById("searchInput");

    const query = input.value.trim();

    if (!query) {

        loadProducts();

        return;
    }

    showLoading();

    try {

        const response = await fetch(
            `${API_BASE}/search?q=${encodeURIComponent(query)}`
        );

        if (!response.ok) {
            throw new Error("Search failed");
        }

        const data = await response.json();

        displayProducts(data.products);

        updateResultCount(data.count);

    } catch (error) {

        console.error("Search error:", error);

        showError("Something went wrong while searching.");
    }
}


// ============================================================
// Load Products by Category
// ============================================================

async function loadCategory(category) {

    showLoading();

    try {

        const response = await fetch(
            `${API_BASE}/category/${encodeURIComponent(category)}`
        );

        if (!response.ok) {
            throw new Error("Category request failed");
        }

        const data = await response.json();

        displayProducts(data.products);

        updateResultCount(data.count);

    } catch (error) {

        console.error("Category error:", error);

        showError("Unable to load this category.");
    }
}


// ============================================================
// Load Statistics
// ============================================================

async function loadStatistics() {

    try {

        const response = await fetch(
            `${API_BASE}/statistics`
        );

        if (!response.ok) {
            throw new Error("Statistics request failed");
        }

        const data = await response.json();

        document.getElementById("totalProducts").textContent =
            data.total_products;

        document.getElementById("amazonCheaper").textContent =
            data.amazon_cheaper;

        document.getElementById("flipkartCheaper").textContent =
            data.flipkart_cheaper;

        document.getElementById("samePrice").textContent =
            data.same_price;

    } catch (error) {

        console.error("Statistics error:", error);
    }
}


// ============================================================
// Display Products
// ============================================================

function displayProducts(products) {

    const container =
        document.getElementById("productsContainer");

    container.innerHTML = "";

    if (!products || products.length === 0) {

        container.innerHTML = `
            <div class="no-results">
                <h3>No products found</h3>
                <p>Try another product name.</p>
            </div>
        `;

        return;
    }


    products.forEach(function (product) {

        const card = createProductCard(product);

        container.appendChild(card);

    });
}


// ============================================================
// Create Product Card
// ============================================================

function createProductCard(product) {

    const card = document.createElement("div");

    card.className = "product-card";


    // --------------------------------------------------------
    // Prices
    // --------------------------------------------------------

    const amazonPrice =
        Number(product.amazon_price) || 0;

    const flipkartPrice =
        Number(product.flipkart_price) || 0;


    // --------------------------------------------------------
    // Determine Cheaper Platform
    // --------------------------------------------------------

    let cheaperPlatform = "Same Price";

    let savings = 0;

    if (amazonPrice < flipkartPrice) {

        cheaperPlatform = "Amazon";

        savings = flipkartPrice - amazonPrice;

    } else if (flipkartPrice < amazonPrice) {

        cheaperPlatform = "Flipkart";

        savings = amazonPrice - flipkartPrice;
    }


    // --------------------------------------------------------
    // Image
    // --------------------------------------------------------

    const imageUrl =
        product.amazon_image ||
        product.flipkart_image ||
        "";


    // --------------------------------------------------------
    // Image HTML
    // --------------------------------------------------------

    let imageHTML = "";

    if (imageUrl) {

        imageHTML = `
            <img
                src="${escapeHTML(imageUrl)}"
                alt="Product"
                class="product-image"
                onerror="this.style.display='none'"
            >
        `;

    } else {

        imageHTML = `
            <div class="image-placeholder">
                🛒
            </div>
        `;
    }


    // --------------------------------------------------------
    // Amazon Link
    // --------------------------------------------------------

    let amazonLink = "";

    if (product.amazon_url) {

        amazonLink = `
            <a
                href="${escapeHTML(product.amazon_url)}"
                target="_blank"
                rel="noopener noreferrer"
                class="view-button amazon-button"
            >
                View on Amazon
            </a>
        `;
    }


    // --------------------------------------------------------
    // Flipkart Link
    // --------------------------------------------------------

    let flipkartLink = "";

    if (product.flipkart_url) {

        flipkartLink = `
            <a
                href="${escapeHTML(product.flipkart_url)}"
                target="_blank"
                rel="noopener noreferrer"
                class="view-button flipkart-button"
            >
                View on Flipkart
            </a>
        `;
    }


    // --------------------------------------------------------
    // Cheaper Badge
    // --------------------------------------------------------

    let badgeHTML = "";

    if (cheaperPlatform === "Amazon") {

        badgeHTML = `
            <div class="cheaper-badge amazon-badge">
                🏆 Amazon is cheaper
            </div>
        `;

    } else if (cheaperPlatform === "Flipkart") {

        badgeHTML = `
            <div class="cheaper-badge flipkart-badge">
                🏆 Flipkart is cheaper
            </div>
        `;

    } else {

        badgeHTML = `
            <div class="cheaper-badge same-badge">
                Same Price
            </div>
        `;
    }


    // --------------------------------------------------------
    // Product Card HTML
    // --------------------------------------------------------

    card.innerHTML = `

        ${badgeHTML}

        <div class="product-image-container">
            ${imageHTML}
        </div>

        <div class="product-content">

            <h3 class="product-name">
                ${escapeHTML(product.amazon_product || "Product")}
            </h3>

            <p class="category">
                Category: ${escapeHTML(product.category || "Other")}
            </p>


            <div class="comparison">


                <!-- AMAZON -->

                <div class="store amazon-store">

                    <div class="store-name">
                        🟠 Amazon
                    </div>

                    <div class="price">
                        ₹${formatPrice(amazonPrice)}
                    </div>

                    ${amazonLink}

                </div>


                <!-- FLIPKART -->

                <div class="store flipkart-store">

                    <div class="store-name">
                        🔵 Flipkart
                    </div>

                    <div class="price">
                        ₹${formatPrice(flipkartPrice)}
                    </div>

                    ${flipkartLink}

                </div>


            </div>


            <div class="product-footer">

                <span>
                    💰 Savings:
                    <strong>₹${formatPrice(savings)}</strong>
                </span>

                <span>
                    Similarity:
                    <strong>
                        ${formatSimilarity(product.similarity_score)}
                    </strong>
                </span>

            </div>

        </div>
    `;


    return card;
}


// ============================================================
// Format Price
// ============================================================

function formatPrice(price) {

    return Number(price).toLocaleString("en-IN", {
        maximumFractionDigits: 0
    });
}


// ============================================================
// Format Similarity
// ============================================================

function formatSimilarity(score) {

    const value = Number(score);

    if (isNaN(value)) {
        return "N/A";
    }

    return (value * 100).toFixed(1) + "%";
}


// ============================================================
// Update Result Count
// ============================================================

function updateResultCount(count) {

    const element =
        document.getElementById("resultCount");

    element.textContent =
        `${count} product${count === 1 ? "" : "s"} found`;
}


// ============================================================
// Loading Message
// ============================================================

function showLoading() {

    const container =
        document.getElementById("productsContainer");

    container.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading products...</p>
        </div>
    `;
}


// ============================================================
// Error Message
// ============================================================

function showError(message) {

    const container =
        document.getElementById("productsContainer");

    container.innerHTML = `
        <div class="error-message">
            <h3>⚠️ Error</h3>
            <p>${escapeHTML(message)}</p>
        </div>
    `;
}


// ============================================================
// Escape HTML
// ============================================================

function escapeHTML(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
