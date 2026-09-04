(function () {
    var buttons = document.querySelectorAll('[data-lang-btn]');
    var translatable = document.querySelectorAll('[data-fr][data-en]');

    function setLanguage(lang) {
        translatable.forEach(function (el) {
            var text = lang === 'en' ? el.getAttribute('data-en') : el.getAttribute('data-fr');
            if (text !== null) {
                el.textContent = text;
            }
        });

        buttons.forEach(function (btn) {
            var isActive = btn.getAttribute('data-lang-btn') === lang;
            btn.classList.toggle('is-active', isActive);
        });

        document.documentElement.setAttribute('lang', lang);
    }

    buttons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            setLanguage(btn.getAttribute('data-lang-btn'));
        });
    });

    // French is the default language on load.
    setLanguage('fr');
})();