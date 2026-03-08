mobileMenuBtn.addEventListener("click", function () {
    if (mainNav.style.display === "none" || mainNav.style.display === "") {
        mainNav.style.display = "block";
        mobileMenuBtn.innerHTML = "&#10005;";
    } else {
        mainNav.style.display = "none";
        mobileMenuBtn.innerHTML = "&#9776;";
    }
}
);

window.addEventListener("resize", function () {
    if (window.innerWidth > 768) {
        mainNav.style.display = "flex";
        mobileMenuBtn.innerHTML = "&#9776;";
    } else {
        mainNav.style.display = "none";
        mobileMenuBtn.innerHTML = "&#9776;";
    }
}
);