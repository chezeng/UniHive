document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.mark-button').forEach(button => {
        button.addEventListener('click', async function(event) {
            event.preventDefault();

            const dataId = button.getAttribute('data-id');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            try {
                const response = await fetch(markButtonUrl, {
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
                    const markButton = document.querySelector(`.mark-button[data-id="${dataId}"]`);
                    const unmarkButton = document.querySelector(`.unmark-button[data-id="${dataId}"]`);

                    markButton.style.display='none';
                    unmarkButton.style.display='block';
                } else {
                    alert(data.message || 'Error saving post');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while saving.');
            }
        })
    });

    document.querySelectorAll('.unmark-button').forEach(button => {
        button.addEventListener('click', async function(event) {
            event.preventDefault();

            const dataId = button.getAttribute('data-id');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            try {
                const response = await fetch(unmarkButtonUrl, {
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
                    const markButton = document.querySelector(`.mark-button[data-id="${dataId}"]`);
                    const unmarkButton = document.querySelector(`.unmark-button[data-id="${dataId}"]`);

                    markButton.style.display='block';
                    unmarkButton.style.display='none';
                } else {
                    alert(data.message || 'Error saving post');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while saving.');
            }
        })
    });

    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            console.log('clicked');
    
            const dataId = button.getAttribute('data-id');
            const editSpace = document.querySelector(`.edit-space[data-id="${dataId}"]`);
            const contentSpace = document.querySelector(`.content-space[data-id="${dataId}"]`);
            const textSpace = document.querySelector(`.text-space[data-id="${dataId}"]`);
    
            if (editSpace.style.display === 'none' || editSpace.style.display === '') {
                editSpace.style.display = 'block';
                textSpace.value = contentSpace.innerText.trim();
                contentSpace.style.display = 'none';
            } else {
                editSpace.style.display = 'none';
                contentSpace.style.display = 'block';
            }
        });
    });

    document.querySelectorAll('.edit-space form').forEach(form => {
        form.addEventListener('submit', async function(event) {
            event.preventDefault();
    
            const textSpace = form.querySelector('.text-space');
            const dataId = textSpace.getAttribute('data-id');
            const content = textSpace.value;
            
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            try {
                const response = await fetch(savePostUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({
                        post_id: dataId,
                        content: content
                    })
                });

                const data = await response.json();
                
                if (data.status === 'success') {
                    const contentSpace = document.querySelector(`.content-space[data-id="${dataId}"]`);
                    contentSpace.innerText = content;
                    
                    const editSpace = document.querySelector(`.edit-space[data-id="${dataId}"]`);
                    editSpace.style.display = 'none';
                    contentSpace.style.display = 'block';
                    
                } else {
                    alert(data.message || 'Error saving post');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while saving.');
            }
        });
    });

    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', async function(event) {
            event.preventDefault();

            console.log('oii')
    
            const dataId = button.getAttribute('data-id');
            
            // Get CSRF token from meta tag
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
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
                        likesCountElement.textContent = `❤️ ${data.likes_count}`;
                        likeButton.style.display = 'none';
                        unlikeButton.style.display = 'block';
                    }

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
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
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
                        likesCountElement.textContent = `❤️ ${data.likes_count}`;
                        likeButton.style.display = 'block';
                        unlikeButton.style.display = 'none';
                    }
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