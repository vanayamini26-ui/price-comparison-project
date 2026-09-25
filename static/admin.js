let allAdminProducts = [];
let editingProductId = null;
let deletingProductId = null;


/* =========================
   PASSWORD TOGGLE
   ========================= */

function togglePassword(inputId, button) {
    const input = document.getElementById(inputId);

    if (!input) return;

    input.type = input.type === "password"
        ? "text"
        : "password";
}


/* =========================
   CHECK ADMIN
   ========================= */

async function checkAdminLogin() {
    try {
        const response = await fetch("/api/admin/check", {
            cache: "no-store"
        });

        if (!response.ok) {
            window.location.href = "/admin/login";
            return false;
        }

        const data = await response.json();

        if (!data.authenticated) {
            window.location.href = "/admin/login";
            return false;
        }

        return true;

    } catch (error) {
        console.error("Admin check error:", error);
        window.location.href = "/admin/login";
        return false;
    }
}


/* =========================
   LOAD PRODUCTS
   ========================= */

async function loadAdminProducts() {

    const tbody =
        document.getElementById("adminProductTableBody");

    if (!tbody) return;

    tbody.innerHTML = `
        <tr>
            <td colspan="6" class="no-products">
                Loading products...
            </td>
        </tr>
    `;

    try {

        const response = await fetch(
            "/api/products",
            {
                method: "GET",
                cache: "no-store"
            }
        );

        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const data = await response.json();

        console.log("PriceWise products:", data);

        if (
            !data ||
            data.status !== "success" ||
            !Array.isArray(data.products)
        ) {
            throw new Error(
                "Invalid product API response"
            );
        }

        allAdminProducts = data.products;

        updateStatistics(allAdminProducts);

        renderProducts(allAdminProducts);

    } catch (error) {

        console.error(
            "Could not load admin products:",
            error
        );

        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="no-products">
                    Unable to load products.
                    <br>
                    <small>
                        Please refresh the page.
                    </small>
                </td>
            </tr>
        `;
    }
}


/* =========================
   STATISTICS
   ========================= */

function updateStatistics(products) {

    const total =
        document.getElementById("totalProducts");

    const mobiles =
        document.getElementById("totalMobiles");

    const laptops =
        document.getElementById("totalLaptops");

    const earphones =
        document.getElementById("totalEarphones");


    const mobileCount =
        products.filter(
            p => String(p.category).toLowerCase() === "mobiles"
        ).length;

    const laptopCount =
        products.filter(
            p => String(p.category).toLowerCase() === "laptops"
        ).length;

    const earphoneCount =
        products.filter(
            p => String(p.category).toLowerCase() === "earphones"
        ).length;


    if (total) {
        total.textContent = products.length;
    }

    if (mobiles) {
        mobiles.textContent = mobileCount;
    }

    if (laptops) {
        laptops.textContent = laptopCount;
    }

    if (earphones) {
        earphones.textContent = earphoneCount;
    }
}


/* =========================
   RENDER PRODUCTS
   ========================= */

function renderProducts(products) {

    const tbody =
        document.getElementById("adminProductTableBody");

    if (!tbody) return;


    if (!products.length) {

        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="no-products">
                    No products found.
                </td>
            </tr>
        `;

        return;
    }


    tbody.innerHTML = products.map(product => {

        const id =
            product.id ?? "-";

        const name =
            product.amazon_product ||
            product.flipkart_product ||
            "-";

        const category =
            product.category ||
            "-";

        const amazonPrice =
            formatPrice(product.amazon_price);

        const flipkartPrice =
            formatPrice(product.flipkart_price);


        return `
            <tr>

                <td>
                    ${escapeHtml(id)}
                </td>

                <td class="product-name-cell">
                    ${escapeHtml(name)}
                </td>

                <td>
                    <span class="category-badge">
                        ${escapeHtml(category)}
                    </span>
                </td>

                <td class="price-cell">
                    ${amazonPrice}
                </td>

                <td class="price-cell">
                    ${flipkartPrice}
                </td>

                <td>

                    <div class="admin-actions">

                        <button
                            type="button"
                            class="edit-btn"
                            onclick="openEditProduct(${Number(id)})">
                            Edit
                        </button>

                        <button
                            type="button"
                            class="delete-btn"
                            onclick="openDeleteModal(${Number(id)})">
                            Delete
                        </button>

                    </div>

                </td>

            </tr>
        `;

    }).join("");
}


/* =========================
   FORMAT PRICE
   ========================= */

function formatPrice(price) {

    if (
        price === null ||
        price === undefined ||
        price === ""
    ) {
        return "-";
    }

    const number =
        Number(price);

    if (Number.isNaN(number)) {
        return escapeHtml(price);
    }

    return "₹" +
        number.toLocaleString("en-IN");
}


/* =========================
   SEARCH
   ========================= */

function searchAdminProducts() {

    const input =
        document.getElementById("adminSearch");

    if (!input) return;

    const query =
        input.value.trim().toLowerCase();


    if (!query) {
        renderProducts(allAdminProducts);
        return;
    }


    const filtered =
        allAdminProducts.filter(product => {

            const amazon =
                String(
                    product.amazon_product || ""
                ).toLowerCase();

            const flipkart =
                String(
                    product.flipkart_product || ""
                ).toLowerCase();

            const category =
                String(
                    product.category || ""
                ).toLowerCase();


            return (
                amazon.includes(query) ||
                flipkart.includes(query) ||
                category.includes(query)
            );
        });


    renderProducts(filtered);
}


/* =========================
   ADD PRODUCT
   ========================= */

function openAddProduct() {

    editingProductId = null;

    const modal =
        document.getElementById("productModal");

    const form =
        document.getElementById("productForm");

    const title =
        document.getElementById("productModalTitle");


    if (!modal || !form) return;

    form.reset();

    if (title) {
        title.textContent = "Add Product";
    }

    modal.classList.add("active");
}


/* =========================
   EDIT PRODUCT
   ========================= */

function openEditProduct(productId) {

    const product =
        allAdminProducts.find(
            p => Number(p.id) === Number(productId)
        );


    if (!product) {
        alert("Product not found.");
        return;
    }


    editingProductId =
        Number(productId);


    const modal =
        document.getElementById("productModal");

    const title =
        document.getElementById("productModalTitle");


    if (!modal) return;


    if (title) {
        title.textContent = "Edit Product";
    }


    setValue(
        "productCategory",
        product.category
    );

    setValue(
        "amazonProductName",
        product.amazon_product
    );

    setValue(
        "flipkartProductName",
        product.flipkart_product
    );

    setValue(
        "amazonPrice",
        product.amazon_price
    );

    setValue(
        "flipkartPrice",
        product.flipkart_price
    );

    setValue(
        "productImageUrl",
        product.image_url
    );

    setValue(
        "amazonProductUrl",
        product.amazon_url
    );

    setValue(
        "flipkartProductUrl",
        product.flipkart_url
    );


    modal.classList.add("active");
}


/* =========================
   SET FORM VALUE
   ========================= */

function setValue(id, value) {

    const element =
        document.getElementById(id);

    if (element) {
        element.value =
            value ?? "";
    }
}


/* =========================
   CLOSE PRODUCT MODAL
   ========================= */

function closeProductModal() {

    const modal =
        document.getElementById("productModal");

    if (modal) {
        modal.classList.remove("active");
    }

    editingProductId = null;
}


/* =========================
   DELETE MODAL
   ========================= */

function openDeleteModal(productId) {

    deletingProductId =
        Number(productId);

    const modal =
        document.getElementById("deleteModal");

    if (modal) {
        modal.classList.add("active");
    }
}


function closeDeleteModal() {

    const modal =
        document.getElementById("deleteModal");

    if (modal) {
        modal.classList.remove("active");
    }

    deletingProductId = null;
}


/* =========================
   DELETE
   ========================= */

async function confirmDelete() {

    if (!deletingProductId) {
        return;
    }

    alert(
        "Delete API will be connected next."
    );

    closeDeleteModal();
}


/* =========================
   ADD / EDIT SUBMIT
   ========================= */

async function handleProductSubmit(event) {

    event.preventDefault();

    if (editingProductId) {

        alert(
            "Edit API will be connected next."
        );

    } else {

        alert(
            "Add API will be connected next."
        );
    }
}


/* =========================
   ADMIN LOGOUT
   ========================= */

async function adminLogout() {

    try {

        await fetch(
            "/api/admin/logout",
            {
                method: "POST"
            }
        );

    } catch (error) {

        console.error(
            "Logout error:",
            error
        );
    }

    window.location.href =
        "/admin/login";
}


/* =========================
   ESCAPE HTML
   ========================= */

function escapeHtml(value) {

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


/* =========================
   PAGE INITIALIZATION
   ========================= */

document.addEventListener(
    "DOMContentLoaded",
    async function () {

        const adminSearch =
            document.getElementById("adminSearch");

        const adminTable =
            document.getElementById(
                "adminProductTableBody"
            );


        /*
         * If this is the login page,
         * don't run dashboard code.
         */

        if (!adminSearch && !adminTable) {
            return;
        }


        const loggedIn =
            await checkAdminLogin();


        if (!loggedIn) {
            return;
        }


        if (adminSearch) {

            adminSearch.addEventListener(
                "input",
                searchAdminProducts
            );
        }


        const productForm =
            document.getElementById("productForm");


        if (productForm) {

            productForm.addEventListener(
                "submit",
                handleProductSubmit
            );
        }


        await loadAdminProducts();
    }
);