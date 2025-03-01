/**
 * Enhanced Company Carousel
 * Provides smooth scrolling and interactive features
 */
document.addEventListener('DOMContentLoaded', function() {
    const companyTrack = document.querySelector('.companies-track');
    const companyCards = document.querySelectorAll('.company-card');

    // Add click event to company cards
    companyCards.forEach(card => {
        card.addEventListener('click', function() {
            const companyName = this.querySelector('.company-name').textContent;
            // Navigate to search results for this company
            window.location.href = `/search/?q=${encodeURIComponent(companyName)}`;
        });

        // Add hover effect
        card.addEventListener('mouseenter', function() {
            this.style.cursor = 'pointer';
        });
    });

    // Adjust animation speed based on number of companies
    if (companyCards.length > 15) {
        companyTrack.style.animationDuration = '45s';
    } else if (companyCards.length > 10) {
        companyTrack.style.animationDuration = '35s';
    } else {
        companyTrack.style.animationDuration = '25s';
    }

    // Pause animation on mouse hover
    companyTrack.addEventListener('mouseenter', function() {
        this.style.animationPlayState = 'paused';
    });

    companyTrack.addEventListener('mouseleave', function() {
        this.style.animationPlayState = 'running';
    });
});
