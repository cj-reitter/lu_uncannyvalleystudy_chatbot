document.addEventListener('DOMContentLoaded', function() {
    const surveyForm = document.getElementById('survey_form');
    
    if (surveyForm) {
        surveyForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(surveyForm);
            
            /*const ratingQuestions = ['rq_1', 'rq_2', 'rq_3', 'rq_4', 'rq_5', 'rq_6', 'rq_7', 'rq_8', 'rq_9', 'rq_10'];
            
            let allRatingsAnswered = true;
            
            for (let question of ratingQuestions) {
                if (!formData.get(question)) {
                    allRatingsAnswered = false;
                    break;
                }
            }
            
            if (!allRatingsAnswered) {
                alert('Please answer all rating questions to submit the survey.');
                return;
            }*/
            
            const data = {};
            for (let [key, value] of formData.entries()) {
                if (key !== 'csrfmiddlewaretoken') {
                    data[key] = value;
                }
            }
            
            const csrfToken = formData.get('csrfmiddlewaretoken');
            
            fetch(surveyForm.action || window.location.pathname, {
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
                    window.location.href = '/feedback';
                } else {
                    alert('Error: ' + (data.error || 'There was an error submitting the survey.'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('There was an error submitting the survey. Please try again.');
            });
        });
    }
});
