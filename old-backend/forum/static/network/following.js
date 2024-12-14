document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', async function(event) {
            event.preventDefault();
            console.log('Like button clicked');
    
            const dataId = button.getAttribute('data-id');
            
            const csrfToken = document.querySelector('form [name=csrfmiddlewaretoken]').value;
            
            try {
                const response = await fetch(likePostUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({
                        post_id: dataId
                    })
                });
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    const likesCountElement = document.querySelector(`.likes-count[data-id="${dataId}"]`);
                    const likeButton = document.querySelector(`.like-button[data-id="${dataId}"]`);
                    const unlikeButton = document.querySelector(`.unlike-button[data-id="${dataId}"]`);
                    
                    if (likesCountElement) {
                        console.log("Likes count:", data.likes_count);
                        likesCountElement.textContent = `Likes: ${data.likes_count}`;
                        likeButton.style.display = 'none';
                        unlikeButton.style.display = 'block';
                    }

                    alert(data.message);
                } else {
                    alert(data.message || 'Error saving post');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while saving.');
            }
        });
    });

    document.querySelectorAll('.unlike-button').forEach(button => {
        button.addEventListener('click', async function(event) {
            event.preventDefault();
    
            const dataId = button.getAttribute('data-id');
            
            const csrfToken = document.querySelector('form [name=csrfmiddlewaretoken]').value;
            
            try {
                const response = await fetch(unlikePostUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({
                        post_id: dataId
                    })
                });

                const data = await response.json();
                
                if (data.status === 'success') {
                    const likesCountElement = document.querySelector(`.likes-count[data-id="${dataId}"]`);
                    const likeButton = document.querySelector(`.like-button[data-id="${dataId}"]`);
                    const unlikeButton = document.querySelector(`.unlike-button[data-id="${dataId}"]`);
                    if (likesCountElement) {
                        console.log("Likes count:", data.likes_count);
                        likesCountElement.textContent = `Likes: ${data.likes_count}`;
                        likeButton.style.display = 'block';
                        unlikeButton.style.display = 'none';
                    }

                    alert(data.message);
                } else {
                    alert(data.message || 'Error saving post');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while saving.');
            }
        });
    });
});