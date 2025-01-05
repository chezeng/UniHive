document.addEventListener("DOMContentLoaded", function() {
    const fetchPost = async (url, postId, content = null) => {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const body = content ? { post_id: postId, content } : { post_id: postId };
        
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(body)
            });
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing your request.');
            return null;
        }
    };

    // Editting
    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const dataId = button.dataset.id;
            const editSpace = document.querySelector(`.edit-space[data-id="${dataId}"]`);
            const contentSpace = document.querySelector(`.content-space[data-id="${dataId}"]`);
            const textSpace = document.querySelector(`.text-space[data-id="${dataId}"]`);

            const isHidden = editSpace.style.display === 'none' || !editSpace.style.display;
            editSpace.style.display = isHidden ? 'block' : 'none';
            contentSpace.style.display = isHidden ? 'none' : 'block';
            if (isHidden) textSpace.value = contentSpace.innerText.trim();
        });
    });

    // Save the editting
    document.querySelectorAll('.edit-space form').forEach(form => {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            const textSpace = form.querySelector('.text-space');
            const dataId = textSpace.dataset.id;
            const content = textSpace.value;

            const data = await fetchPost(savePostUrl, dataId, content);
            if (data?.status === 'success') {
                const contentSpace = document.querySelector(`.content-space[data-id="${dataId}"]`);
                contentSpace.innerText = content;
                
                const editSpace = document.querySelector(`.edit-space[data-id="${dataId}"]`);
                editSpace.style.display = 'none';
                contentSpace.style.display = 'block';
            }
        });
    });

    // Liked / Unliked
    const handleLikeAction = async (button, isLike) => {
        const dataId = button.dataset.id;
        const url = isLike ? likePostUrl : unlikePostUrl;
        
        const data = await fetchPost(url, dataId);
        if (data?.status === 'success') {
            const likesCountElement = document.querySelector(`.likes-count[data-id="${dataId}"]`);
            const likeButton = document.querySelector(`.like-button[data-id="${dataId}"]`);
            const unlikeButton = document.querySelector(`.unlike-button[data-id="${dataId}"]`);
            
            if (likesCountElement) {
                likesCountElement.textContent = `❤️ ${data.likes_count}`;
                likeButton.style.display = isLike ? 'none' : 'block';
                unlikeButton.style.display = isLike ? 'block' : 'none';
            }
        }
    };

    // Liked Event
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            handleLikeAction(button, true);
        });
    });

    document.querySelectorAll('.unlike-button').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            handleLikeAction(button, false);
        });
    });
});