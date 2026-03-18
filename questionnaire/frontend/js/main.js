document.addEventListener("DOMContentLoaded", () => {

    // РЕГИСТРАЦИЯ
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

    // ЛОГИН
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
            window.location.href = "/hello"
        } else {
            alert(data.detail);
        }
    });

    // КОД ПОДТВЕРЖДЕНИЯ
    const inputs = document.querySelectorAll('.code input');
    inputs.forEach((input, index) =>{
        input.addEventListener('input', () => {
            input.value = input.value.replace(/\D/g, '');
            if(input.value && index < inputs.length - 1){
                inputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', (e) => {
            if(e.key === "Backspace" && !input.value && index > 0){
                inputs[index - 1].focus();
            }
        });
    });

    const confirmBtn = document.querySelector(".code-btn");
    confirmBtn?.addEventListener("click", async () => {

        const inputs = document.querySelectorAll(".code input");

        let activation_code = "";
        inputs.forEach(input => activation_code += input.value);

        localStorage.setItem("reset_code", activation_code);

        let email = localStorage.getItem("confirm_email");
        let url = "/confirm";

        if(localStorage.getItem("reset_email")){
            email = localStorage.getItem("reset_email");
            url = "/reset/confirm";
        }

        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: email,
                activation_code: activation_code
            })
        });

        const data = await response.json();

        if(response.ok){
            if(localStorage.getItem("reset_email")){
                alert("Пароль успешно изменён!");
                localStorage.removeItem("reset_email");
                localStorage.removeItem("reset_code");
            } else {
                alert("Регистрация завершена!");
                window.location.href = "/hello";
            }
        } else {
            alert(data.detail);
        }
    });


    //ЯНДЕКС OAUTH
    const oauthQueryParams = {
        client_id: "ВАШ_CLIENT_ID",
        response_type: "code",
        redirect_uri: "http://localhost:8000/auth/yandex/callback"
    };

    const tokenPageOrigin = window.location.origin;

    if (window.YaAuthSuggest) {
        window.YaAuthSuggest.init(
            oauthQueryParams,
            tokenPageOrigin,
            {
                view: "button",
                parentId: "buttonContainerId",
                buttonSize: 'm',
                buttonView: 'main',
                buttonTheme: 'light',
                buttonBorderRadius: "0",
                buttonIcon: 'ya',
            }
        )
        .then(({handler}) => {
            document
                .getElementById("buttonContainerId")
                ?.addEventListener("click", handler);
        })
        .catch(error => console.log('Ошибка OAuth', error));
    }

});

// СБРОС ПАРОЛЯ
document.getElementById("passwordForm")?.addEventListener("submit", async function(e){
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("confirm_password").value;

    if(!email.includes("@")){
        alert("Email должен содержать @");
        return;
    }

    if(password !== confirm_password){
        alert("Пароли не совпадают");
        return;
    }

    try{
        const response = await fetch("/reset", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: email,
                new_password: password
            })
        });

        const data = await response.json();

        if(response.ok){
            alert("Код отправлен на email");
            localStorage.setItem("reset_email", email);
            window.location.href = "/reset"; 
        } else {
            alert(data.detail);
        }

    } catch(err){
        console.error(err);
        alert("Ошибка запроса");
    }
});