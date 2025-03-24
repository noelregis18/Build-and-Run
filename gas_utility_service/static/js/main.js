// Main JavaScript for Gas Utility Customer Service application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Add animations to cards
    const animateCards = document.querySelectorAll('.animate-card');
    animateCards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.classList.add('shadow-lg');
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('shadow-lg');
            this.style.transform = 'translateY(0)';
        });
    });

    // Handle service request priority change
    const prioritySelect = document.getElementById('id_priority');
    if (prioritySelect) {
        prioritySelect.addEventListener('change', function() {
            const value = this.value;
            const emergencyWarning = document.getElementById('emergency-warning');
            
            if (value === 'emergency' && !emergencyWarning) {
                const warningDiv = document.createElement('div');
                warningDiv.id = 'emergency-warning';
                warningDiv.className = 'alert alert-danger mt-2';
                warningDiv.innerHTML = '<strong>Warning:</strong> Emergency requests are for situations that pose an immediate safety risk. For gas leaks or similar emergencies, please also call our emergency hotline at <strong>1-800-GAS-LEAK</strong>.';
                
                this.parentNode.appendChild(warningDiv);
            } else if (value !== 'emergency' && emergencyWarning) {
                emergencyWarning.remove();
            }
        });
    }
});
