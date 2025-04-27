// scripts.js

// Set the current year in the footer
document.addEventListener("DOMContentLoaded", () => {
    const yearElement = document.getElementById("year");
    const currentYear = new Date().getFullYear();
    if (yearElement) {
        yearElement.textContent = currentYear;
    }
});

// Highlight the active navigation link
function highlightActiveNav() {
    const navLinks = document.querySelectorAll("nav a");
    const currentPage = window.location.pathname.split("/").pop();

    navLinks.forEach(link => {
        if (link.getAttribute("href") === currentPage) {
            link.style.backgroundColor = "#004D40";
            link.style.borderRadius = "5px";
        }
    });
}
highlightActiveNav();

// Scroll-to-top button
const scrollTopBtn = document.createElement("button");
scrollTopBtn.textContent = "↑";
scrollTopBtn.style.position = "fixed";
scrollTopBtn.style.bottom = "20px";
scrollTopBtn.style.right = "20px";
scrollTopBtn.style.padding = "10px";
scrollTopBtn.style.display = "none";
scrollTopBtn.style.borderRadius = "50%";
scrollTopBtn.style.backgroundColor = "#00796B";
scrollTopBtn.style.color = "#fff";
scrollTopBtn.style.border = "none";
scrollTopBtn.style.cursor = "pointer";
document.body.appendChild(scrollTopBtn);

window.addEventListener("scroll", () => {
    if (window.scrollY > 200) {
        scrollTopBtn.style.display = "block";
    } else {
        scrollTopBtn.style.display = "none";
    }
});

scrollTopBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
});

// Simple form validation for the Appointment form
const appointmentForm = document.querySelector("#appointmentForm");
if (appointmentForm) {
    appointmentForm.addEventListener("submit", (e) => {
        const name = document.querySelector("#name").value.trim();
        const email = document.querySelector("#email").value.trim();
        let isValid = true;

        if (name === "") {
            alert("Please enter your name.");
            isValid = false;
        }
        if (email === "" || !/^\S+@\S+\.\S+$/.test(email)) {
            alert("Please enter a valid email address.");
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
        }
    });
}
