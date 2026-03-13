document.addEventListener("DOMContentLoaded", () => {

    // Регистрация
    const registerForm = document.getElementById("registerForm");

    registerForm?.addEventListener("submit", async function(e) {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const name = document.getElementById('FirstName').value;
        const SecondName = document.getElementById('SecondName').value;
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm_password").value;

        if(!email.includes("@")){
            alert("Email должен содержать @");
            return;
        }

        if(password !== confirmPassword){
            alert("Пароли не совпадают");
            return;
        }

        const response = await fetch("/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                email: email,
                password: password,
                first_name: name,
                last_name: SecondName
             })
        });

        const data = await response.json();

        if(response.ok){
            localStorage.setItem("confirm_email", email);
            window.location.href="/reset";
        }else{
            alert(data.detail);
        }
    });

    // Логин
    const loginForm = document.getElementById("signon");

    loginForm?.addEventListener("submit", async function(e){
        e.preventDefault();

        const email = document.getElementById("login_email").value;
        const password = document.getElementById("login_password").value;

        const response = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if(response.ok){
            alert("Успешный вход");
        } else {
            alert(data.detail);
        }
    });

    //Код подтверждения
    const inputs = document.querySelectorAll('.code input');
    inputs.forEach((input, index) =>{
        input.addEventListener('input', () => {
            input.value = input.value.replace(/\D/g, '')
            if(input.value && index < inputs.length - 1){
                inputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', (e) => {
            if(e.key === "Backspace" && !input.value && index > 0){
                inputs[index - 1].focus();
            }
        })
    });

    //Код подтверждения
    const confirmBtn = document.querySelector(".code-btn");
    confirmBtn?.addEventListener("click", async () => {

    const inputs = document.querySelectorAll(".code input");

    let activation_code = "";

    inputs.forEach(input => {
        activation_code += input.value;
    });


    const email = localStorage.getItem("confirm_email");

    const response = await fetch("/confirm", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            activation_code: activation_code
        })
    });

    const data = await response.json();

    if(response.ok){
        alert("Регистрация завершена");
        window.location.href="/";
    }else{
        alert(data.detail);
    }

});

    //Сброс пароля
    const form = document.getElementById("emailForm");
    form?.addEventListener("submit", async function(e){
    e.preventDefault();
    const email = document.getElementById("login_email").value;
    
    if(!email.includes("@")){
        alert("Email должен содержать @");
        return;
    }

    try {
        const response = await fetch("/reset", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email })
        });

        const data = await response.json();

        if(response.ok){
            alert("Код для сброса пароля отправлен на email");
            localStorage.setItem("reset_email", email);
            window.location.href = "/reset";
        } else {
            alert(data.detail);
        }

    } catch (err) {
        console.error(err);
        alert("Ошибка при отправке запроса");
    }
});



document.getElementById("passwordForm")?.addEventListener("submit", async function(e){
    e.preventDefault();

    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("confirm_password").value;
    const email = localStorage.getItem("reset_email");

    if(password !== confirm_password){
        return alert("Пароли не совпадают");
    }

    const response = await fetch("/reset/confirm", {  
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            email: email,
            activation_code: localStorage.getItem("reset_code"),
            new_password: password,
            confirm_password: confirm_password
        })
    });

    const data = await response.json();

    if(response.ok){
        alert("Пароль успешно изменён!");

        // переход на страницу
        window.location.href = "/password";

    } else {
        alert(data.detail);
    }
});

});