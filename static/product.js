/* ============================================================
   PRICEWISE - PRODUCT COMPARISON
============================================================ */


/* ============================================================
   LOAD PRODUCT
============================================================ */

async function loadProduct() {

    const container =
        document.getElementById("productContainer");

    try {

        const response =
            await fetch(`/api/products/${productId}`);

        if (!response.ok) {
            throw new Error("Product not found");
        }

        const data =
            await response.json();

        if (
            data.status !== "success" ||
            !data.product
        ) {
            throw new Error("Product not found");
        }

        displayProduct(
            data.product,
            container
        );

    } catch (error) {

        console.error(
            "Product loading error:",
            error
        );

        container.innerHTML = `

            <div class="error-message">

                <h2>
                    Product Not Found
                </h2>

                <p>
                    Sorry, we could not load this product.
                </p>

                <a
                    href="javascript:history.back()"
                    class="error-back"
                >
                    ← Go Back
                </a>

            </div>

        `;
    }
}


/* ============================================================
   DISPLAY PRODUCT
============================================================ */

function displayProduct(
    product,
    container
) {

    const amazonName =
        product.amazon_product || "Amazon Product";

    const flipkartName =
        product.flipkart_product || "Flipkart Product";


    const productName =
        amazonName !== "Amazon Product"
            ? amazonName
            : flipkartName;


    const image =
        product.image ||
        product.amazon_image ||
        product.flipkart_image ||
        "";


    const amazonPrice =
        Number(
            product.amazon_price || 0
        );


    const flipkartPrice =
        Number(
            product.flipkart_price || 0
        );


    let cheaperPlatform = "";

    let savings = 0;


    if (
        amazonPrice > 0 &&
        flipkartPrice > 0
    ) {

        if (
            amazonPrice < flipkartPrice
        ) {

            cheaperPlatform =
                "Amazon";

            savings =
                flipkartPrice -
                amazonPrice;

        } else if (
            flipkartPrice < amazonPrice
        ) {

            cheaperPlatform =
                "Flipkart";

            savings =
                amazonPrice -
                flipkartPrice;

        } else {

            cheaperPlatform =
                "Both";

            savings = 0;
        }
    }


    const amazonUrl =
        product.amazon_url ||
        product.amazon_product_url ||
        product.actual_amazon_url ||
        "#";


    const flipkartUrl =
        product.flipkart_url ||
        product.flipkart_product_url ||
        product.actual_flipkart_url ||
        "#";


    let imageHTML = "";


    if (image) {

        imageHTML = `

            <img
                src="${escapeHTML(image)}"
                alt="${escapeHTML(productName)}"
                class="product-image"
                onerror="this.style.display='none';"
            >

        `;

    } else {

        imageHTML = `

            <div
                style="
                    font-size:80px;
                    color:#9ca3af;
                "
            >
                📦
            </div>

        `;
    }


    let amazonClass = "price-card";

    let flipkartClass = "price-card";


    if (cheaperPlatform === "Amazon") {

        amazonClass += " cheaper";

    } else if (
        cheaperPlatform === "Flipkart"
    ) {

        flipkartClass += " cheaper";
    }


    let cheaperLabel = "";

    if (cheaperPlatform === "Amazon") {

        cheaperLabel = `
            <span class="cheaper-label">
                ✓ Lower Price
            </span>
        `;

    } else if (
        cheaperPlatform === "Flipkart"
    ) {

        cheaperLabel = `
            <span class="cheaper-label">
                ✓ Lower Price
            </span>
        `;
    }


    let savingsText = "";


    if (savings > 0) {

        savingsText = `

            You can save

            <span class="savings-amount">
                ₹${formatPrice(savings)}
            </span>

            by shopping on
            <strong>${cheaperPlatform}</strong>.

        `;

    } else {

        savingsText = `
            Both platforms have the same price.
        `;
    }


    container.innerHTML = `

        <div class="product-details">


            <!-- PRODUCT IMAGE -->

            <div class="product-image-section">

                ${imageHTML}

            </div>



            <!-- PRODUCT INFORMATION -->

            <div class="product-info">


                <span class="product-category">

                    ${escapeHTML(
                        product.category || "Product"
                    )}

                </span>


                <h1 class="product-title">

                    ${escapeHTML(productName)}

                </h1>



                <!-- PRICE CARDS -->

                <div class="price-comparison">


                    <div class="${amazonClass}">

                        <div class="store-name">
                            Amazon
                        </div>

                        <div class="store-price">

                            ₹${formatPrice(
                                amazonPrice
                            )}

                        </div>

                        ${
                            cheaperPlatform === "Amazon"
                                ? cheaperLabel
                                : ""
                        }

                    </div>



                    <div class="${flipkartClass}">

                        <div class="store-name">
                            Flipkart
                        </div>

                        <div class="store-price">

                            ₹${formatPrice(
                                flipkartPrice
                            )}

                        </div>

                        ${
                            cheaperPlatform === "Flipkart"
                                ? cheaperLabel
                                : ""
                        }

                    </div>


                </div>



                <!-- SAVINGS -->

                <div class="savings-box">

                    ${savingsText}

                </div>



                <!-- SHOP BUTTONS -->

                <div class="shop-buttons">


                    <a
                        href="${escapeHTML(amazonUrl)}"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="shop-button amazon-button"
                    >

                        🛒 Shop on Amazon

                    </a>


                    <a
                        href="${escapeHTML(flipkartUrl)}"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="shop-button flipkart-button"
                    >

                        🛒 Shop on Flipkart

                    </a>


                </div>


            </div>


        </div>

    `;
}


/* ============================================================
   FORMAT PRICE
============================================================ */

function formatPrice(price) {

    if (
        !price ||
        isNaN(price)
    ) {

        return "0";
    }

    return Number(price).toLocaleString(
        "en-IN"
    );
}


/* ============================================================
   ESCAPE HTML
============================================================ */

function escapeHTML(value) {

    return String(value || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


/* ============================================================
   START
============================================================ */

loadProduct();