document.addEventListener('DOMContentLoaded', function() {
    const consentCheckbox = document.getElementById('consent_checkbox');
    const beginButton = document.getElementById('begin_button');

    beginButton.addEventListener('click', function(event) {
        if (!consentCheckbox.checked) {
            event.preventDefault();
            alert('Please click the consent checkbox.');
            return false;
        }
    });
});