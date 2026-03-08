
function selectFormat(element, format) {
    const formatCards = document.getElementsByClassName('format-card');
    for (let i = 0; i < formatCards.length; i++) {
        formatCards[i].classList.remove('selected');
    }

    element.classList.add('selected');
    document.getElementById('talk-format').value = format;
    document.getElementById('talk-format').required = true;
}

document.getElementById('s-technical').addEventListener('change', function () {
    const technicalDetails = document.getElementById('technical-details');
    if (this.checked) {
        technicalDetails.style.display = 'block';
    } else {
        technicalDetails.style.display = 'none';
    }
});

$(".chosen-select").chosen({
    no_results_text: "Oops, nothing found!"
})

console.log('welcome to speaker js');

document.addEventListener('DOMContentLoaded', function() {
    const selectElement = document.getElementById('s-track');

    function getSelectedTracks() {
        // For Chosen, we use .val() via jQuery or just plain value
        const selectedValues = $('#s-track').val();  // This gives an array of selected values
        console.log('Selected tracks:', selectedValues);
        return selectedValues;
    }

    // Listen to change events
    $('#s-track').on('change', getSelectedTracks);

    // Optionally, you can call it manually
    // getSelectedTracks();
});
