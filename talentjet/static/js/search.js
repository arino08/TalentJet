// Search functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Search JS loaded');

    const searchInput = document.getElementById('searchInput');
    const searchForm = document.getElementById('searchForm');
    const searchFormContainer = document.getElementById('searchFormContainer');
    const searchOverlay = document.querySelector('.search-overlay');
    const body = document.body;

    // Clear any previous state on page load
    body.classList.remove('search-focused');

    if (searchInput) {
        console.log('Search input found');

        function enableSearchMode() {
            console.log('Enabling search mode');
            body.classList.add('search-focused');
        }

        function disableSearchMode() {
            console.log('Disabling search mode');
            body.classList.remove('search-focused');
        }

        // Add click handler for better mobile support
        searchInput.addEventListener('click', enableSearchMode);

        // Add focus handler
        searchInput.addEventListener('focus', enableSearchMode);

        // Handle overlay click
        if (searchOverlay) {
            searchOverlay.addEventListener('click', function() {
                disableSearchMode();
                searchInput.blur();
            });
        }

        // Handle escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && body.classList.contains('search-focused')) {
                disableSearchMode();
                searchInput.blur();
            }
        });

        // Prevent form submission on enter if input is empty
        if (searchForm) {
            searchForm.addEventListener('submit', function(e) {
                if (!searchInput.value.trim()) {
                    e.preventDefault();
                }
            });
        }
    } else {
        console.error('Search input not found');
    }
});
