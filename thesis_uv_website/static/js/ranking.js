document.addEventListener('DOMContentLoaded', function() {
    let currentImageName = null;
    
    const submitBtn = document.getElementById('submit_ranking_btn');
    const messageDiv = document.getElementById('ranking_message');
    
    loadNextImage();
    
    submitBtn.addEventListener('click', function() {
        const selectedRanking = document.querySelector('input[name="ranking"]:checked');
        
        if (!selectedRanking) {
            alert('Please select a ranking before submitting.');
            return;
        }
        
        if (!currentImageName) {
            alert('Error: No image selected.');
            return;
        }
        
        // Submit ranking
        submitRanking(currentImageName, selectedRanking.value);
    });
    
    function loadNextImage() {
        fetch('/ranking/get-next-image/')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (data.completed) {
                        alert('Congratulations! You have ranked all avatars. You may now exit the page.');
                        document.getElementById('current_image').style.display = 'none';
                        document.querySelector('.ranking_form').style.display = 'none';
                        submitBtn.disabled = true;
                    } else {
                        currentImageName = data.image_name;
                        document.getElementById('current_image').src = data.image_url;
                        
                        const progressText = document.getElementById('progress_text');
                        progressText.textContent = `${data.progress.ranked}/${data.progress.total}`;
                        
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
