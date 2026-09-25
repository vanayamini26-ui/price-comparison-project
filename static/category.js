// ============================================================
// PRICEWISE - CATEGORY PRODUCTS PAGE
// ============================================================


let categoryProducts = [];


// ============================================================
// PAGE LOAD
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        setupCategoryPage();

    }
);


// ============================================================
// SETUP
// ============================================================

function setupCategoryPage() {

    const title =
        document.getElementById("categoryTitle");

    const description =
        document.getElementById(
            "categoryDescription"
        );


    const category =
        selectedCategory;


    if (category === "All") {

        title.textContent =
            "All Products";

        description.textContent =
            "Compare electronic products from trusted stores.";

    }

    else {

        title.textContent =
            category;

        description.textContent =
            `Find and compare ${category.toLowerCase()} prices.`;

    }


    loadCategoryProducts(category);


    const search =
        document.getElementById(
            "categorySearch"
        );


    search.addEventListener(
        "input",
        function () {

            filterProducts(
                search.value
            );

        }
    );

}


// ============================================================
// LOAD CATEGORY
// ============================================================

async function loadCategoryProducts(category) {

    showLoading();


    try {

        let url;


        if (category === "All") {

            url =
                "/api/products";

        }

        else {

            url =
                `/api/category/${encodeURIComponent(category)}`;

        }


        const response =
            await fetch(url);


        if (!response.ok) {

            throw new Error(
                "Unable to load products"
            );

        }


        const data =
            await response.json();


        categoryProducts =
            data.products || [];


        displayProducts(
            categoryProducts
        );

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
        document.getElementById(
            "productsContainer"
        );


    container.innerHTML = "";


    if (!products.length) {

        container.innerHTML = `

            <div class="no-products">

                <div
                    style="
                        font-size:40px;
                        margin-bottom:10px;
                    "
                >
                    🔍
                </div>

                <h3>
                    No products found
                </h3>

                <p>
                    Try another search.
                </p>

            </div>

        `;

        return;

    }


    products.forEach(
        function (product) {

            container.appendChild(
                createProductCard(product)
            );

        }
    );

}


// ============================================================
// CREATE PRODUCT CARD
// ============================================================

function createProductCard(product) {

    const card =
        document.createElement("div");

    card.className =
        "product-card";


    const name =
        product.amazon_product ||
        product.flipkart_product ||
        "Electronic Product";


    const category =
        product.category ||
        "Electronics";


    const amazonPrice =
        Number(
            product.amazon_price || 0
        );


    const flipkartPrice =
        Number(
            product.flipkart_price || 0
        );


    let savings = 0;

    let cheaper = "";


    if (
        amazonPrice > 0 &&
        flipkartPrice > 0
    ) {

        if (
            amazonPrice <
            flipkartPrice
        ) {

            savings =
                flipkartPrice -
                amazonPrice;

            cheaper =
                "Amazon";

        }

        else if (
            flipkartPrice <
            amazonPrice
        ) {

            savings =
                amazonPrice -
                flipkartPrice;

            cheaper =
                "Flipkart";

        }

    }


    const image =
        product.image_url ||
        product.product_image ||
        product.amazon_image ||
        product.flipkart_image ||
        "";


    card.innerHTML = `

        <div class="product-image">

            ${
                image

                ?

                `
                <img
                    src="${escapeHTML(image)}"
                    alt="${escapeHTML(name)}"
                    loading="lazy"
                    onerror="this.style.display='none'; this.nextElementSibling.style.display='block';"
                >

                <div
                    class="image-placeholder"
                    style="display:none;"
                >
                    ${getIcon(category)}
                </div>
                `

                :

                `
                <div class="image-placeholder">
                    ${getIcon(category)}
                </div>
                `
            }

        </div>


        <div class="product-content">

            <h3>
                ${escapeHTML(name)}
            </h3>


            <span class="product-category">
                ${escapeHTML(category)}
            </span>


            <div class="prices">


                <div class="price-box">

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


                <div class="price-box">

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
                <div class="saving">

                    💰 Save
                    ${formatPrice(savings)}
                    with ${cheaper}

                </div>
                `

                :

                `
                <div class="saving">

                    Compare prices before buying

                </div>
                `
            }


            <a
                href="/product/${product.id || ""}"
                class="details-button"
            >
                View Comparison →
            </a>


        </div>

    `;


    return card;

}


// ============================================================
// SEARCH / FILTER
// ============================================================

function filterProducts(query) {

    const search =
        query
            .toLowerCase()
            .trim();


    if (!search) {

        displayProducts(
            categoryProducts
        );

        return;

    }


    const filtered =
        categoryProducts.filter(
            function (product) {

                const amazon =
                    String(
                        product.amazon_product || ""
                    ).toLowerCase();


                const flipkart =
                    String(
                        product.flipkart_product || ""
                    ).toLowerCase();


                return (
                    amazon.includes(search) ||
                    flipkart.includes(search)
                );

            }
        );


    displayProducts(filtered);

}


// ============================================================
// ICON
// ============================================================

function getIcon(category) {

    const value =
        String(category)
            .toLowerCase();


    if (
        value.includes("mobile")
    ) {

        return "📱";

    }


    if (
        value.includes("laptop")
    ) {

        return "💻";

    }


    if (
        value.includes("earphone")
    ) {

        return "🎧";

    }


    return "🛍️";

}


// ============================================================
// PRICE
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


    return (
        "₹" +
        number.toLocaleString("en-IN")
    );

}


// ============================================================
// ESCAPE HTML
// ============================================================

function escapeHTML(value) {

    if (
        value === null ||
        value === undefined
    ) {

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
// LOADING
// ============================================================

function showLoading() {

    const container =
        document.getElementById(
            "productsContainer"
        );


    container.innerHTML = `

        <div class="loading">

            <div
                style="
                    font-size:35px;
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


    container.innerHTML = `

        <div class="error-message">

            <div
                style="
                    font-size:35px;
                    margin-bottom:10px;
                "
            >
                ⚠️
            </div>

            ${escapeHTML(message)}

        </div>

    `;

}