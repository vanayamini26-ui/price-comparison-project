// ============================================================
// PRICEWISE - PRODUCT PAGE SCRIPT
// ============================================================


// ============================================================
// GLOBAL DATA
// ============================================================

let allProducts = [];


// ============================================================
// PAGE LOAD
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    loadProducts();

});


// ============================================================
// LOAD ALL PRODUCTS
// ============================================================

async function loadProducts() {

    showLoading();

    try {

        const response = await fetch("/api/products");

        if (!response.ok) {
            throw new Error("Unable to load products");
        }

        const data = await response.json();

        allProducts = data.products || [];

        displayProducts(allProducts);

    }

    catch (error) {

        console.error(error);

        showError(
            "Unable to load products. Please try again."
        );

    }

}


// ============================================================
// DISPLAY PRODUCTS
// ============================================================

function displayProducts(products) {

    const container =
        document.getElementById("productsContainer");

    if (!container) {
        return;
    }


    container.innerHTML = "";


    if (!products || products.length === 0) {

        container.innerHTML = `
            <div class="no-products">
                <h3>No products found</h3>
                <p>Try another product name or category.</p>
            </div>
        `;

        updateResultCount();

        return;

    }


    products.forEach(function (product) {

        const card =
            createProductCard(product);

        container.appendChild(card);

    });


    // IMPORTANT:
    // We intentionally do NOT show the product count.

    updateResultCount();

}


// ============================================================
// CREATE PRODUCT CARD
// ============================================================

function createProductCard(product) {

    const card =
        document.createElement("div");

    card.className = "product-card";


    const amazonPrice =
        Number(product.amazon_price || 0);

    const flipkartPrice =
        Number(product.flipkart_price || 0);


    let cheaperPlatform = "";

    let savings = 0;


    if (
        amazonPrice > 0 &&
        flipkartPrice > 0
    ) {

        if (amazonPrice < flipkartPrice) {

            cheaperPlatform = "Amazon";

            savings =
                flipkartPrice - amazonPrice;

        }

        else if (flipkartPrice < amazonPrice) {

            cheaperPlatform = "Flipkart";

            savings =
                amazonPrice - flipkartPrice;

        }

        else {

            cheaperPlatform = "Same Price";

            savings = 0;

        }

    }


    const imageUrl =
        product.image_url ||
        product.product_image ||
        product.amazon_image ||
        product.flipkart_image ||
        "";


    const productName =
        product.amazon_product ||
        product.flipkart_product ||
        "Electronic Product";


    const category =
        product.category ||
        "Electronics";


    const amazonLink =
        product.amazon_url ||
        product.amazon_link ||
        "#";


    const flipkartLink =
        product.flipkart_url ||
        product.flipkart_link ||
        "#";


    card.innerHTML = `

        <div class="product-image-container">

            ${
                imageUrl
                ?
                `
                <img
                    src="${escapeHTML(imageUrl)}"
                    alt="${escapeHTML(productName)}"
                    loading="lazy"
                    onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
                >

                <div
                    class="image-fallback"
                    style="
                        display:none;
                        align-items:center;
                        justify-content:center;
                        width:100%;
                        height:100%;
                        font-size:45px;
                    "
                >
                    ${getCategoryIcon(category)}
                </div>
                `
                :
                `
                <div
                    class="image-fallback"
                    style="
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        width:100%;
                        height:100%;
                        font-size:45px;
                    "
                >
                    ${getCategoryIcon(category)}
                </div>
                `
            }

        </div>


        <div class="product-info">

            <h3>
                ${escapeHTML(productName)}
            </h3>


            <span class="product-category">
                ${escapeHTML(category)}
            </span>


            <div class="store-comparison">


                <div class="store-block">

                    <span>
                        Amazon
                    </span>

                    <strong>
                        ${
                            amazonPrice > 0
                            ? formatPrice(amazonPrice)
                            : "Not available"
                        }
                    </strong>

                </div>


                <div class="store-block">

                    <span>
                        Flipkart
                    </span>

                    <strong>
                        ${
                            flipkartPrice > 0
                            ? formatPrice(flipkartPrice)
                            : "Not available"
                        }
                    </strong>

                </div>


            </div>


            ${
                savings > 0
                ?
                `
                <div class="savings">

                    💰 Save ${formatPrice(savings)}
                    with ${cheaperPlatform}

                </div>
                `
                :
                `
                <div class="savings">

                    Compare prices before buying

                </div>
                `
            }


            <div
                class="product-links"
                style="
                    display:grid;
                    grid-template-columns:1fr 1fr;
                    gap:8px;
                "
            >

                <a
                    href="${safeLink(amazonLink)}"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="compare-button"
                >
                    Amazon
                </a>


                <a
                    href="${safeLink(flipkartLink)}"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="compare-button"
                >
                    Flipkart
                </a>

            </div>


        </div>

    `;


    return card;

}


// ============================================================
// SEARCH PRODUCTS
// ============================================================

async function searchProducts() {

    const searchInput =
        document.getElementById("searchInput");

    if (!searchInput) {
        return;
    }


    const query =
        searchInput.value.trim();


    if (!query) {

        loadProducts();

        return;

    }


    showLoading();


    try {

        const response =
            await fetch(
                `/api/search?q=${encodeURIComponent(query)}`
            );


        if (!response.ok) {
            throw new Error("Search failed");
        }


        const data =
            await response.json();


        displayProducts(
            data.products || []
        );

    }

    catch (error) {

        console.error(error);

        showError(
            "Unable to search products."
        );

    }

}


// ============================================================
// CATEGORY FILTER
// ============================================================

async function loadCategory(category) {

    if (category === "all") {

        loadProducts();

        return;

    }


    showLoading();


    try {

        const response =
            await fetch(
                `/api/category/${encodeURIComponent(category)}`
            );


        if (!response.ok) {
            throw new Error("Category loading failed");
        }


        const data =
            await response.json();


        displayProducts(
            data.products || []
        );

    }

    catch (error) {

        console.error(error);

        showError(
            "Unable to load this category."
        );

    }

}


// ============================================================
// SELECT CATEGORY
// ============================================================

function selectCategory(button, category) {

    setActiveCategory(category);


    const searchInput =
        document.getElementById("searchInput");


    if (searchInput) {

        searchInput.value = "";

    }


    if (category === "all") {

        loadProducts();

    }

    else {

        loadCategory(category);

    }


    // Scroll to products

    const productsSection =
        document.querySelector(".products-section");


    if (productsSection) {

        setTimeout(function () {

            productsSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }, 100);

    }

}


// ============================================================
// ACTIVE CATEGORY
// ============================================================

function setActiveCategory(category) {

    const buttons =
        document.querySelectorAll(
            ".category-card"
        );


    buttons.forEach(function (button) {

        button.classList.remove("active");


        const text =
            button.textContent
                .toLowerCase()
                .trim();


        if (
            category === "all" &&
            (
                text.includes("all products") ||
                text.includes("all categories")
            )
        ) {

            button.classList.add("active");

        }


        else if (
            category === "Mobiles" &&
            text.includes("mobiles")
        ) {

            button.classList.add("active");

        }


        else if (
            category === "Laptops" &&
            text.includes("laptops")
        ) {

            button.classList.add("active");

        }


        else if (
            category === "Earphones" &&
            text.includes("earphones")
        ) {

            button.classList.add("active");

        }

    });

}


// ============================================================
// CLEAR SEARCH
// ============================================================

function clearSearch() {

    const searchInput =
        document.getElementById("searchInput");


    if (searchInput) {

        searchInput.value = "";

    }


    setActiveCategory("all");

    loadProducts();

}


// ============================================================
// RESULT TEXT
// ============================================================

// IMPORTANT:
// This function does NOT display the number of products.

function updateResultCount() {

    const resultCount =
        document.getElementById("resultCount");


    if (!resultCount) {
        return;
    }


    resultCount.textContent =
        "Compare prices and find the right product.";

}


// ============================================================
// LOADING
// ============================================================

function showLoading() {

    const container =
        document.getElementById(
            "productsContainer"
        );


    if (!container) {
        return;
    }


    container.innerHTML = `

        <div class="loading">

            <div
                style="
                    font-size:30px;
                    margin-bottom:10px;
                "
            >
                ⏳
            </div>

            Loading products...

        </div>

    `;

}


// ============================================================
// ERROR
// ============================================================

function showError(message) {

    const container =
        document.getElementById(
            "productsContainer"
        );


    if (!container) {
        return;
    }


    container.innerHTML = `

        <div class="error-message">

            <div
                style="
                    font-size:30px;
                    margin-bottom:10px;
                "
            >
                ⚠️
            </div>

            <p>
                ${escapeHTML(message)}
            </p>

            <button
                onclick="loadProducts()"
                style="
                    margin-top:15px;
                    padding:10px 18px;
                    border:none;
                    border-radius:8px;
                    background:#159b91;
                    color:white;
                    cursor:pointer;
                "
            >
                Try Again
            </button>

        </div>

    `;


    updateResultCount();

}


// ============================================================
// PRICE FORMAT
// ============================================================

function formatPrice(price) {

    const number =
        Number(price);


    if (
        !Number.isFinite(number) ||
        number <= 0
    ) {

        return "₹--";

    }


    return "₹" +
        number.toLocaleString("en-IN");

}


// ============================================================
// CATEGORY ICON
// ============================================================

function getCategoryIcon(category) {

    const value =
        String(category)
            .toLowerCase();


    if (value.includes("mobile")) {

        return "📱";

    }


    if (value.includes("laptop")) {

        return "💻";

    }


    if (
        value.includes("earphone") ||
        value.includes("audio")
    ) {

        return "🎧";

    }


    return "🛍️";

}


// ============================================================
// ESCAPE HTML
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


// ============================================================
// SAFE LINK
// ============================================================

function safeLink(url) {

    if (!url) {

        return "#";

    }


    const value =
        String(url).trim();


    if (
        value.startsWith("http://") ||
        value.startsWith("https://")
    ) {

        return escapeHTML(value);

    }


    return "#";

}