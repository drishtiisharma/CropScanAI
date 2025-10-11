const toggle = document.getElementById("theme-toggle");
const icon = toggle.querySelector("i");

// Apply saved theme on load
const savedTheme = localStorage.getItem("theme");
if (savedTheme === "dark") {
  document.body.classList.add("dark-mode");
  icon.classList.replace("fa-sun", "fa-moon");
}

// Handle click
toggle.addEventListener("click", () => {
  const darkMode = document.body.classList.toggle("dark-mode");

  if (darkMode) {
    icon.classList.replace("fa-sun", "fa-moon");
    localStorage.setItem("theme", "dark");
  } else {
    icon.classList.replace("fa-moon", "fa-sun");
    localStorage.setItem("theme", "light");
  }
});
