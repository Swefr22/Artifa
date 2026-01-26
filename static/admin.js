/* ARTIFA FEST - Custom Admin JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    // Add smooth animations to elements
    const elements = document.querySelectorAll('input, textarea, select, button, a.button');
    
    elements.forEach(el => {
        el.addEventListener('focus', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });
    
    // Add loading state to form submission
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('input[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Processing...';
                submitBtn.style.opacity = '0.6';
            }
        });
    });
    
    // Enhance table rows with hover effects
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseover', function() {
            this.style.backgroundColor = 'hsl(240, 13%, 20%)';
        });
        row.addEventListener('mouseout', function() {
            this.style.backgroundColor = 'hsl(240, 13%, 20%)';
        });
    });
    
    // Add confirmation for delete links
    const deleteLinks = document.querySelectorAll('a.deletelink');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // Highlight required fields
    const requiredFields = document.querySelectorAll('[aria-required="true"]');
    requiredFields.forEach(field => {
        const label = field.parentElement.querySelector('label');
        if (label) {
            label.innerHTML += ' <span style="color: #e02401; font-weight: bold;">*</span>';
        }
    });
    
    // Add visual feedback for form errors
    const errorElements = document.querySelectorAll('.errorlist');
    errorElements.forEach(error => {
        error.style.animation = 'slideDown 0.3s ease';
    });
    
    // Make action checkboxes more visible
    const actionCheckboxes = document.querySelectorAll('input[name="_selected_action"]');
    actionCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                this.parentElement.style.backgroundColor = 'rgba(224, 36, 1, 0.1)';
            } else {
                this.parentElement.style.backgroundColor = 'transparent';
            }
        });
    });
    
    // Add tooltips
    const helpTexts = document.querySelectorAll('.help-text, .helptext');
    helpTexts.forEach(text => {
        text.addEventListener('mouseover', function() {
            this.style.color = '#ffc107';
        });
        text.addEventListener('mouseout', function() {
            this.style.color = 'hsl(240, 5%, 65%)';
        });
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    console.log('ARTIFA FEST Admin Initialized');
});

/* Animation keyframes */
const style = document.createElement('style');
style.textContent = `
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    /* Glitch effect for headers */
    @keyframes glitch {
        0% {
            text-shadow: -2px 0 #e02401, 2px 0 #ffc107;
        }
        14% {
            text-shadow: -2px 0 #e02401, 2px 0 #ffc107;
        }
        15% {
            text-shadow: 2px 0 #e02401, -2px 0 #ffc107;
        }
        49% {
            text-shadow: 2px 0 #e02401, -2px 0 #ffc107;
        }
        50% {
            text-shadow: -2px 0 #e02401, 2px 0 #ffc107;
        }
        100% {
            text-shadow: -2px 0 #e02401, 2px 0 #ffc107;
        }
    }
`;
document.head.appendChild(style);
