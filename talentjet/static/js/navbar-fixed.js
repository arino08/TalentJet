/**
 * Fixed navbar script that ensures the navbar is always visible
 */
document.addEventListener('DOMContentLoaded', function() {
    // Get the navbar element
    const navbar = document.querySelector('.navbar');

    // Make sure navbar is always visible
    if (navbar) {
        navbar.style.opacity = '1';
        navbar.style.transform = 'translateY(0)';
    }

    // Remove any scroll listeners that might hide the navbar
    window.removeEventListener('scroll', hideNavbarOnScroll);

    // Placeholder for any potential hiding function
    function hideNavbarOnScroll() {
        // This function is intentionally empty to override any previous listeners
        console.log("Navbar hiding prevented");
    }

    // Add scroll behavior to just add shadow on scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 10) {
            navbar.classList.add('shadow-sm');
        } else {
            navbar.classList.remove('shadow-sm');
        }
    });
});
