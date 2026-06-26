/**
 * Determines if consent checkbox is clicked by user on the home page before continuing to the study
 */

document.addEventListener('DOMContentLoaded', function() {
    const consentCheckbox = document.getElementById('consent_checkbox');
    const beginButton = document.getElementById('begin_button');

    // Prevents begin study button from redirecting the user and alerting them to click the consent
    //  checkbox if unchecked
    beginButton.addEventListener('click', function(event) {
        if (!consentCheckbox.checked) {
            event.preventDefault();
            alert('Please click the consent checkbox.');
            return false;
        }
    });
});