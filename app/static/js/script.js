document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const form = document.querySelector('form');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            const inputs = form.querySelectorAll('input[type="number"]');
            let hasError = false;
            
            inputs.forEach(input => {
                // Basic validation for empty fields
                if (input.value.trim() === '') {
                    hasError = true;
                }
                
                // For numeric values, ensure they're valid
                if (input.name === 'age' && (parseFloat(input.value) < 0 || parseFloat(input.value) > 120)) {
                    hasError = true;
                    alert('Please enter a valid age (0-120)');
                }
                
                if (input.name !== 'age' && parseFloat(input.value) < 0) {
                    hasError = true;
                    alert('Values cannot be negative');
                }
            });
            
            if (hasError) {
                event.preventDefault();
            }
        });
    }
    
    // Highlight the active navigation link
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.fontWeight = 'bold';
            link.style.textDecoration = 'underline';
        }
    });
});