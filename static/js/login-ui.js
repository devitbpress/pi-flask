document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/get-sign", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: email,
                password: password,
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const products = await response.json();

        if (products.status === "success") {
            window.location = "/kalkulasi-model";
            localStorage.setItem("spiganeca10", products.sid);
        } else {
            document.getElementById("span-indikator").textContent = "Email / Kata Sandi Salah";
        }
    } catch (error) {
        console.error(error);
    }
});

const setHeight = () => document.getElementById("container").style.setProperty("--vh", `${window.innerHeight * 0.01}px`);

window.addEventListener("resize", setHeight);
