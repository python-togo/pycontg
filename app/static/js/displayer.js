document.getElementById('s-tshirt').addEventListener('change', function () {
    const technicalDetails = document.getElementById('tshirt-size');
    if (this.checked) {
        technicalDetails.style.display = 'block';
    } else {
        technicalDetails.style.display = 'none';
    }
});