const checkbox = document.getElementById('consent_checkbox');
const endBody = document.querySelector('.end_body');

endBody.style.display = 'none';

checkbox.addEventListener('change', () => {
    endBody.style.display = checkbox.checked ? 'block' : 'none';
});
