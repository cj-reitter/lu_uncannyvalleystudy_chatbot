/**
 * Determines if survey explanation is displayed on the endpage or not depending on the consent checkbox
 */

const checkbox = document.getElementById('consent_checkbox');
const endBody = document.querySelector('.end_body');

endBody.style.display = 'none'; // Defaults to not displaying the survey explanation

// If checkbox is clicked/unclicked, survey explanation is displayed/hidden respectively
checkbox.addEventListener('change', () => {
    endBody.style.display = checkbox.checked ? 'block' : 'none';
});
