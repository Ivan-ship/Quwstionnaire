document.getElementById("registerForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const email = document.getElementById("email").value;
    if(!email.includes("@")){
        alert("Email должен обязательно иметь символ @")
        return;
    }

    const password = document.getElementById("password").value;

    const confirmPassword = document.getElementById("confirm_password").value;
    if(password !== confirmPassword){
        alert("Пароли не совпадают")
        return;
    }

    const response = await fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });
    const data = await response.json();
    document.getElementById("result").innerText = data.message || data.detail;
});

