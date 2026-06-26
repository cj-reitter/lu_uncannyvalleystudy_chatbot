/**
 * Loads images from media dataset and sends user ranking data to ranking database
 */

document.addEventListener('DOMContentLoaded', function() {

    let currentImageName = null;
    
    const submitBtn = document.getElementById('submit_ranking_btn');
    const messageDiv = document.getElementById('ranking_message');
    
    loadNextImage(); // Loads first image from the media dataset when the page loads
    
    // Submits user ranking when submit button clicked
    submitBtn.addEventListener('click', function() {
        const selectedRanking = document.querySelector('input[name="ranking"]:checked');
        
        // Alerts user if they haven't chosen a ranking
        if (!selectedRanking) {
            alert('Please select a ranking before submitting.');
            return;
        }
        
        // Alerts user if no image has loaded yet
        if (!currentImageName) {
            alert('Error: No image selected.');
            return;
        }
        
        submitRanking(currentImageName, selectedRanking.value); // Submit ranking
    });
    
    function loadNextImage() {
        /**
         * Loads random unranked image to the UI
         */

        // Fetches new random image from the ranking model
        fetch('/ranking/get-next-image/')
            .then(response => response.json())
            .then(data => {
                if (data.success) {

                    // Alerts user if all images hae been ranked and stops displaying ranking form
                    if (data.completed) {
                        alert('Congratulations! You have ranked all avatars. You may now exit the page.');
                        document.getElementById('current_image').style.display = 'none';
                        document.querySelector('.ranking_form').style.display = 'none';
                        submitBtn.disabled = true;
                    } else {

                        // Sets displayed image to the newly generated image
                        currentImageName = data.image_name;
                        document.getElementById('current_image').src = data.image_url;
                        
                        // Adds ranked image count to the image ranking progress
                        const progressText = document.getElementById('progress_text');
                        progressText.textContent = `${data.progress.ranked}/${data.progress.total}`;
                        
                        // Keeps unranked images loaded
                        document.querySelectorAll('input[name="ranking"]').forEach(el => el.checked = false);
                        messageDiv.textContent = '';
                    }
                } else {
                    alert('Error: ' + (data.error || 'Failed to load image.'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error loading image. Please try again.');
            });
    }
    
    function submitRanking(imageName, rankingValue) {
        /**
         * Submits users ranking for a given image in the media dataset when they hit submit
         * @param {string} imageName File name of the image being ranked
         * @param {number} rankingValue Human likeness ranking given to the image (10-100)
         */

        // Sends ranking data to ranking database
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        
        fetch('/ranking/submit-ranking/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                image_name: imageName,
                ranking: rankingValue
            })
        })
            .then(response => response.json())

            // Loads new unranked image if user response successfully submitted
            .then(data => {
                if (data.success) {
                    setTimeout(loadNextImage, 1000);
                } else {
                    alert('Error: ' + (data.error || 'Failed to save ranking.'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error submitting ranking. Please try again.');
            });
    }
    
});
