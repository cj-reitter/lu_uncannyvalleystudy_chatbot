document.addEventListener('DOMContentLoaded', function() {
    const feedbackForm = document.getElementById('feedback_form');
    
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(feedbackForm);
            
            const data = {};
            for (let [key, value] of formData.entries()) {
                if (key !== 'csrfmiddlewaretoken') {
                    data[key] = value;
                }
            }
            
            const csrfToken = formData.get('csrfmiddlewaretoken');
            
            fetch(feedbackForm.action || window.location.pathname, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/home';
                } else {
                    alert('Error: ' + (data.error || 'There was an error submitting your feedback.'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('There was an error submitting your feedback. Please try again.');
            });
        });
    }
});
