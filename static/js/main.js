// ARTIFA FEST - Main JavaScript
// Enhanced Stranger Things Theme with Interactive Features

document.addEventListener('DOMContentLoaded', function() {
    initNavbarScroll();
    initSmoothScroll();
    initFormValidation();
    initTimelineAnimation();
    initCardAnimations();
});

// Navbar Scroll Effect
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// Smooth Scroll for Links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// Form Validation
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Timeline Animation on Scroll
function initTimelineAnimation() {
    const timelineItems = document.querySelectorAll('.timeline-item');
    
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    timelineItems.forEach(item => {
        observer.observe(item);
    });
}

// Card Animations
function initCardAnimations() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach((card, index) => {
        card.style.animation = `slideIn 0.6s ease forwards`;
        card.style.animationDelay = `${index * 0.1}s`;
    });
}

// Add to Cart / Register Button Handler
document.querySelectorAll('.btn-danger, .btn-outline-danger').forEach(btn => {
    btn.addEventListener('click', function(e) {
        if (!this.form) {
            e.preventDefault();
            // Add ripple effect
            createRipple(e, this);
        }
    });
});

// Ripple Effect
function createRipple(event, element) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');
    
    element.appendChild(ripple);
    
    setTimeout(() => ripple.remove(), 600);
}

// Dynamic Theme Toggle (Optional)
function toggleTheme() {
    const body = document.body;
    body.classList.toggle('stranger-things-theme');
    localStorage.setItem('theme', body.classList.contains('stranger-things-theme') ? 'dark' : 'light');
}

// Load saved theme preference
window.addEventListener('load', function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.remove('stranger-things-theme');
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Alt + T to toggle theme
    if (e.altKey && e.key === 't') {
        toggleTheme();
    }
});

// Prevent console errors
console.log('%cARTIFA FEST - Stranger Things Theme Loaded', 'color: #ff0000; font-size: 16px; font-weight: bold; text-shadow: 0 0 10px #ff0000;');
