// -----------------------------
// LOGIN
// -----------------------------
document.getElementById("login").addEventListener("click", async () => {
  const passwordInput = document.getElementById("password");
  const status = document.getElementById("status");
  const password = passwordInput.value;

  status.innerText = "Logging in...";

  try {
    const res = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ password })
    });

    if (!res.ok) {
      status.innerText = "Wrong password";
      return;
    }

    const data = await res.json();
    localStorage.setItem("token", data.token);

    status.innerText = "Logged in!";
  } catch (err) {
    status.innerText = "Login failed";
    console.error(err);
  }
});

// -----------------------------
// LOAD SESSIONS (PROTECTED)
// -----------------------------
async function loadSessions() {
  const status = document.getElementById("status");
  const output = document.getElementById("output");
  const token = localStorage.getItem("token");

  if (!token) {
    status.innerText = "Please log in first";
    return;
  }

  status.innerText = "Loading sessions...";

  try {
    const res = await fetch("http://127.0.0.1:8000/sessions", {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (!res.ok) {
      status.innerText = "Access denied";
      return;
    }

    const data = await res.json();

    status.innerText = "Sessions loaded";
    output.innerText = JSON.stringify(data, null, 2);
  } catch (err) {
    status.innerText = "Failed to load sessions";
    console.error(err);
  }
}

// -----------------------------
// BUTTON WIRING
// -----------------------------
document
  .getElementById("loadSessions")
  .addEventListener("click", loadSessions);
