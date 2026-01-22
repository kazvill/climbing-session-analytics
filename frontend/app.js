const API_URL = "https://climbing-session-analytics.fly.dev"

// If token already exists → skip login
if (window.location.pathname.includes("index")) {
  const token = localStorage.getItem("token")
  if (token) {
    window.location.href = "dashboard.html"
  }
}

const loginBtn = document.getElementById("loginBtn")

if (loginBtn) {
  loginBtn.addEventListener("click", async () => {
    const password = document.getElementById("password").value
    const errorEl = document.getElementById("error")

    errorEl.innerText = ""

    try {
      const res = await fetch(
        `${API_URL}/auth/login?password=${encodeURIComponent(password)}`,
        { method: "POST" }
      )

      if (!res.ok) throw new Error()

      const data = await res.json()
      localStorage.setItem("token", data.token)

      window.location.href = "dashboard.html"
    } catch {
      errorEl.innerText = "Incorrect password"
    }
  })
}
