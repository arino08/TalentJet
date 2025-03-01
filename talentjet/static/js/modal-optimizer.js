/**
 * Modal Optimizer - Improves performance of Bootstrap modals
 */
document.addEventListener('DOMContentLoaded', function() {
    // Get all modals on the page
    const modals = document.querySelectorAll('.modal');

    // Apply optimization techniques to each modal
    modals.forEach(modal => {
        // Use createDocumentFragment for better performance
        const fragment = document.createDocumentFragment();

        // Cache modal content
        let cachedContent = null;

        // Apply optimizations
        modal.addEventListener('show.bs.modal', function() {
            // Force GPU acceleration
            this.style.transform = 'translateZ(0)';
            this.style.willChange = 'transform, opacity';

            // Reduce browser reflow operations
            this.style.contain = 'layout paint';

            // Display content from cache if available
            if (cachedContent) {
                const modalBody = this.querySelector('.modal-body');
                if (modalBody && !modalBody.children.length) {
                    modalBody.appendChild(cachedContent.cloneNode(true));
                }
            }
        });

        // Cache content on first open
        modal.addEventListener('shown.bs.modal', function() {
            if (!cachedContent) {
                const modalBody = this.querySelector('.modal-body');
                if (modalBody) {
                    cachedContent = modalBody.cloneNode(true);
                }
            }

            // Reset will-change to free up resources
            setTimeout(() => {
                this.style.willChange = 'auto';
            }, 300);
        });

        // Cleanup on hide
        modal.addEventListener('hidden.bs.modal', function() {
            this.style.transform = '';
            this.style.contain = '';
        });
    });
});
