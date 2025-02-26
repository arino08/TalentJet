// Optional enhanced search animations
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchForm = document.getElementById('searchForm');
    const searchWrapper = document.querySelector('.mega-search-wrapper');

    if (searchInput && searchWrapper) {
        // Add extra animations on focus if desired
        searchInput.addEventListener('focus', function() {
            // You could add additional classes here for more dramatic effects
            searchWrapper.classList.add('search-focused');

            // You could also animate other elements if desired
            document.querySelector('.hero-title').style.opacity = '0.5';
            document.querySelector('.hero-subtitle').style.opacity = '0.5';
        });

        // Remove animations on blur
        searchInput.addEventListener('blur', function() {
            searchWrapper.classList.remove('search-focused');

            document.querySelector('.hero-title').style.opacity = '1';
            document.querySelector('.hero-subtitle').style.opacity = '1';
        });
    }
});
