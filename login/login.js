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