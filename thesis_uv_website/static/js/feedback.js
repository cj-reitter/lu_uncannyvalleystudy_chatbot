document.addEventListener('DOMContentLoaded', function() {
    /**
     * Sends pretesting feedback to feedback database when participants hit submit button, and redirect
     *  them to the ranking page
     */
    const feedbackForm = document.getElementById('feedback_form');
    
    if (feedbackForm) {

        // Records participant responses to pretesting feedback questions when they hit submit
        feedbackForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(feedbackForm);
            
            const data = {};
            for (let [key, value] of formData.entries()) {
                if (key !== 'csrfmiddlewaretoken') {
                    data[key] = value;
                }
            }
            
            // Sends pretesting feedback data to the feedback database
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

            // Redirects users to ranking page if pretesting feedback successfully submitted
            .then(data => {
                if (data.success) {
                    window.location.href = '/ranking';
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
