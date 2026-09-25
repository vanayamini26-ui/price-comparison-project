// ============================================
// PAGE ELEMENTS
// ============================================

const signupBox = document.getElementById("signupBox");
const signinBox = document.getElementById("signinBox");


// ============================================
// SHOW SIGN UP
// ============================================

function showSignup() {

    signupBox.classList.remove("hidden");
    signinBox.classList.add("hidden");

}


// ============================================
// SHOW SIGN IN
// ============================================

function showSignin() {

    signupBox.classList.add("hidden");
    signinBox.classList.remove("hidden");

}


// ============================================
// SHOW / HIDE PASSWORD
// ============================================

function togglePassword(inputId, button) {

    const passwordInput =
        document.getElementById(inputId);

    const eyeIcon =
        button.querySelector("svg");


    if (passwordInput.type === "password") {

        passwordInput.type = "text";

        button.setAttribute(
            "aria-label",
            "Hide password"
        );

        eyeIcon.innerHTML = `
            <path
                d="M3 3l18 18"
            ></path>

            <path
                d="M10.6 10.6a2 2 0 0 0 2.8 2.8"
            ></path>

            <path
                d="M9.9 4.2A10.7 10.7 0 0 1 12 4c6.5 0 10 8 10 8a17.2 17.2 0 0 1-3.1 4.4"
            ></path>

            <path
                d="M6.1 6.1C3.4 8.1 2 12 2 12s3.5 8 10 8a10.7 10.7 0 0 0 4.1-.8"
            ></path>
        `;

    }

    else {

        passwordInput.type = "password";

        button.setAttribute(
            "aria-label",
            "Show password"
        );

        eyeIcon.innerHTML = `
            <path
                d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"
            ></path>

            <circle
                cx="12"
                cy="12"
                r="3"
            ></circle>
        `;

    }

}


// ============================================
// CHECK EXISTING USER
// ============================================

const savedUser = localStorage.getItem("pricewiseUser");

if (savedUser) {

    showSignin();

}


// ============================================
// SIGN UP
// ============================================

document
    .getElementById("signupForm")
    .addEventListener("submit", function(event) {

        event.preventDefault();

        const name =
            document.getElementById("signupName").value.trim();

        const email =
            document.getElementById("signupEmail").value.trim();

        const password =
            document.getElementById("signupPassword").value;

        const message =
            document.getElementById("signupMessage");


        if (password.length < 6) {

            message.textContent =
                "Password must contain at least 6 characters.";

            message.style.color = "#dc2626";

            return;

        }


        const user = {

            name: name,

            email: email,

            password: password

        };


        localStorage.setItem(
            "pricewiseUser",
            JSON.stringify(user)
        );


        message.textContent =
            "Account created successfully!";

        message.style.color = "#16a34a";


        setTimeout(function() {

            document.getElementById("signinEmail").value =
                email;

            showSignin();

        }, 800);

    });


// ============================================
// SIGN IN
// ============================================

document
    .getElementById("signinForm")
    .addEventListener("submit", function(event) {

        event.preventDefault();

        const email =
            document.getElementById("signinEmail").value.trim();

        const password =
            document.getElementById("signinPassword").value;

        const message =
            document.getElementById("signinMessage");


        const storedUser =
            localStorage.getItem("pricewiseUser");


        if (!storedUser) {

            message.textContent =
                "Please create an account first.";

            message.style.color = "#dc2626";

            showSignup();

            return;

        }


        const user =
            JSON.parse(storedUser);


        if (
            email === user.email &&
            password === user.password
        ) {

            localStorage.setItem(
                "pricewiseLoggedIn",
                "true"
            );


            message.textContent =
                "Sign in successful!";

            message.style.color = "#16a34a";


            setTimeout(function() {

                window.location.href = "/products";

            }, 500);

        }

        else {

            message.textContent =
                "Incorrect email or password.";

            message.style.color = "#dc2626";

        }

    });