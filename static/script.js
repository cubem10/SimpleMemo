async function register() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const result = await fetch("/register", {
        method: "POST", 
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    });
    const data = await result.json()
    alert(data.message);
}

async function change_login_message() {
    const token = localStorage.getItem("token");
    if (!token) {
        document.getElementById("login_text").innerHTML = "Login / Register";
        return;
    }
    const result = await fetch("/user", {
        method: "GET", 
        headers: {"Content-Type": "application/json",
                  "Authorization": `Bearer ${token}`
        }
    })
    const data = await result.json();
    document.getElementById("login_text").innerHTML = "Hello " + data.username;
}

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const result = await fetch("/login", {
        method: "POST", 
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    });
    const data = await result.json();
    alert(data.message);
    localStorage.setItem("token", data.token);
    change_login_message();
    loadMemos();
}

async function logout() {
    localStorage.setItem("token", "");
    change_login_message();
    document.getElementById("memos").innerHTML = "";
}

async function saveMemo() {
    const token = localStorage.getItem("token");
    const content = document.getElementById("memo").value;
    const requestBody = JSON.stringify({content});
    const result = await fetch("/memo", {
        method: "POST", 
        headers: {
            "Content-Type": "application/json", 
            "Authorization": `Bearer ${token}`
        }, 
        body: requestBody
    })
    const data = await result.json();
    alert(data.message);
    loadMemos();
}

async function loadMemos() {
    const token = localStorage.getItem("token");

    const result = await fetch("/memos", {
        method: "GET", 
        headers: {"Authorization": `Bearer ${token}`}
    });

    const data = await result.json();
    const memoList = document.getElementById("memos");
    memoList.innerHTML = "";

    data.forEach(element => {
        const memoItem = document.createElement("p");
        memoItem.textContent = element.content;
        memoList.appendChild(memoItem);
    });
}

window.onload = function() {
    const token = localStorage.getItem("token");
    change_login_message();
    if (token) loadMemos();
}

const inputField = document.getElementById("memos");
const charCountDisplay = document.getElementById("charCount");
const maxLength = inputField.maxLength;

inputField.addEventListener("input", () => {
    const currentLength = inputField.value.length;
    charCountDisplay.innerHTML = `${currentLength} / ${maxLength}`;
})