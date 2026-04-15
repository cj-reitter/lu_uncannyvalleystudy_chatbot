document.addEventListener('DOMContentLoaded', function() {
    const consentCheckbox = document.getElementById('consent_checkbox');
    const beginButton = document.getElementById('begin_button');
    const errorMessage = document.getElementById('begin_error');

    errorMessage.style.display = 'none';

    consentCheckbox.addEventListener('change', function() {
        if (this.checked) {
            errorMessage.style.display = 'none';
        }
    });

    beginButton.addEventListener('click', function(event) {
        if (!consentCheckbox.checked) {
            event.preventDefault();
            errorMessage.style.display = 'block';
            return false;
        }
    });
});