// document.getElementById('sponsorship-level').addEventListener('change', function () {
//     const inkindOption = document.getElementById('inkind-option');

//     inkindOption.style.display = 'none';

//     if (this.value === 'inkind') {
//         inkindOption.style.display = 'block';
//     }
// });

document.addEventListener("DOMContentLoaded", function () {
    const input = document.querySelector("#contact-phone");

    const iti = window.intlTelInput(input, {
        initialCountry: "auto",
        utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@17/build/js/utils.js",
        geoIpLookup: function (callback) {
            fetch('https://ipapi.co/json')
                .then(res => res.json())
                .then(data => callback(data.country_code))
                .catch(() => callback('TG'));
        },
        nationalMode: false,
        preferredCountries: ['tg', 'bj', 'gh', 'fr', 'us']
    });

    const form = document.querySelector("#unique-form");
    const errorMessage = document.createElement("div");
    errorMessage.id = "phone-error";
    errorMessage.style.color = "red";
    errorMessage.style.marginTop = "5px";
    input.parentNode.insertBefore(errorMessage, input.nextSibling);

    form.addEventListener("submit", function (e) {
        if (iti.isValidNumber()) {
            input.value = iti.getNumber();
            errorMessage.textContent = ""; // Clear error message
        } else {
            errorMessage.textContent = "Please enter a valid phone number.";
            e.preventDefault();
        }
    });
});
