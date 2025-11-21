// Signature Extractor Landing Page - Interactive JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive elements
    initNavigation();
    initFAQ();
    initScrollAnimations();
    initHeroAnimations();
    initMobileMenu();
    initFormSubmissions();
    initPricingToggle();
    initTestimonialCarousel();
});

// Navigation functionality
function initNavigation() {
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('.nav-menu a');
    
    // Add scroll effect to navbar
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });

    // Smooth scrolling for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId.startsWith('#')) {
                const targetSection = document.querySelector(targetId);
                if (targetSection) {
                    targetSection.scrollIntoView({ 
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// FAQ accordion functionality
function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', () => {
            const answer = item.querySelector('.faq-answer');
            const icon = question.querySelector('i');
            
            // Close all other FAQ items
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.querySelector('.faq-answer').classList.remove('active');
                    otherItem.querySelector('.faq-question i').classList.remove('active');
                }
            });
            
            // Toggle current item
            answer.classList.toggle('active');
            icon.classList.toggle('active');
        });
    });
}

// Scroll animations for elements
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);
    
    // Observe all elements with scroll-reveal class
    document.querySelectorAll('.scroll-reveal, .feature-card, .use-case-card, .testimonial-card, .pricing-card').forEach(el => {
        observer.observe(el);
    });
    
    // Special handling for workflow steps
    document.querySelectorAll('.step').forEach((step, index) => {
        setTimeout(() => {
            step.style.opacity = '1';
            step.style.transform = 'translateY(0)';
        }, index * 200);
    });
}

// Hero section animations
function initHeroAnimations() {
    // Animate workflow steps in sequence
    const workflowSteps = document.querySelectorAll('.workflow-step');
    let delay = 0;
    
    workflowSteps.forEach((step, index) => {
        setTimeout(() => {
            step.style.opacity = '1';
            step.style.transform = 'scale(1)';
        }, delay);
        delay += 300;
    });
    
    // Add subtle floating animation to app preview
    const appPreview = document.querySelector('.app-preview');
    if (appPreview) {
        // Already handled in CSS
    }
    
    // Animate intro offer with pulse effect
    const introOffer = document.querySelector('.intro-offer');
    if (introOffer) {
        setInterval(() => {
            introOffer.style.animation = 'none';
            setTimeout(() => {
                introOffer.style.animation = 'pulse 2s infinite';
            }, 10);
        }, 4000);
    }
}

// Mobile menu functionality
function initMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navCta = document.querySelector('.nav-cta');
    
    if (hamburger && navMenu && navCta) {
        hamburger.addEventListener('click', () => {
            navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
            navCta.style.display = navCta.style.display === 'flex' ? 'none' : 'flex';
            
            // Animate hamburger
            hamburger.classList.toggle('active');
        });
        
        // Close menu when clicking on links
        document.querySelectorAll('.nav-menu a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.style.display = 'none';
                navCta.style.display = 'none';
                hamburger.classList.remove('active');
            });
        });
    }
}

// Form submissions (for newsletter signup)
function initFormSubmissions() {
    // Add newsletter form if exists
    const newsletterForm = document.querySelector('#newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value;
            
            if (validateEmail(email)) {
                // Simulate form submission
                showNotification('Thank you for subscribing to our updates!');
                emailInput.value = '';
            } else {
                showNotification('Please enter a valid email address.', 'error');
            }
        });
    }
}

// Pricing toggle functionality
function initPricingToggle() {
    // Add event listeners for pricing plans if needed
    const pricingCards = document.querySelectorAll('.pricing-card');
    
    pricingCards.forEach(card => {
        const ctaButton = card.querySelector('.btn');
        if (ctaButton) {
            ctaButton.addEventListener('click', function(e) {
                if (this.href === '#') {
                    e.preventDefault();
                    // Add purchase flow here
                    showNotification('Redirecting to payment page...');
                    // Simulate redirect
                    setTimeout(() => {
                        alert('Payment flow would open here');
                    }, 1000);
                }
            });
        }
    });
}

// Testimonial carousel functionality
function initTestimonialCarousel() {
    let currentTestimonial = 0;
    const testimonials = document.querySelectorAll('.testimonial-card');
    
    if (testimonials.length > 0) {
        // Auto-rotate testimonials
        setInterval(() => {
            testimonials.forEach(t => t.style.opacity = '0.5');
            testimonials[currentTestimonial].style.opacity = '1';
            testimonials[currentTestimonial].style.transform = 'scale(1.02)';
            
            currentTestimonial = (currentTestimonial + 1) % testimonials.length;
            
            setTimeout(() => {
                testimonials.forEach((t, index) => {
                    if (index !== currentTestimonial) {
                        t.style.transform = 'scale(1)';
                    }
                });
            }, 300);
        }, 5000);
    }
}

// Utility functions
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function showNotification(message, type = 'success') {
    // Remove existing notifications
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'check-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#ff4757' : '#2ed573'};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }
    }, 3000);
}

// Add CSS for notification animations
function addNotificationStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

// Initialize notification styles
addNotificationStyles();

// Feature highlight on hover
function initFeatureHighlights() {
    const features = document.querySelectorAll('.feature-card, .use-case-card');
    
    features.forEach(feature => {
        feature.addEventListener('mouseenter', () => {
            feature.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.15)';
        });
        
        feature.addEventListener('mouseleave', () => {
            feature.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.08)';
        });
    });
}

// Initialize feature highlights
initFeatureHighlights();

// Progressively enhance the page
function progressiveEnhancement() {
    // Add loading states for buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            this.disabled = true;
            
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 2000);
        });
    });
    
    // Add image lazy loading for better performance
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize progressive enhancements
progressiveEnhancement();

// Add scroll progress indicator
function addScrollProgress() {
    const scrollProgress = document.createElement('div');
    scrollProgress.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        z-index: 10001;
        transition: width 0.1s ease;
    `;
    document.body.appendChild(scrollProgress);
    
    window.addEventListener('scroll', () => {
        const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
        scrollProgress.style.width = scrollPercent + '%';
    });
}

// Initialize scroll progress
addScrollProgress();

// Add dynamic copyright year
document.addEventListener('DOMContentLoaded', () => {
    const copyrightYear = document.querySelector('.footer-bottom p');
    if (copyrightYear) {
        const currentYear = new Date().getFullYear();
        copyrightYear.innerHTML = `&copy; ${currentYear} Signature Extractor. All rights reserved.`;
    }
});

// Performance optimization
if ('requestIdleCallback' in window) {
    requestIdleCallback(() => {
        // Non-critical optimizations
        optimizeImages();
        lazyLoadComponents();
    });
} else {
    // Fallback for older browsers
    setTimeout(() => {
        optimizeImages();
        lazyLoadComponents();
    }, 1000);
}

function optimizeImages() {
    // Optimize image loading for better performance
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        if (!img.complete) {
            img.onload = () => img.style.opacity = 1;
            img.style.opacity = 0;
            img.style.transition = 'opacity 0.3s ease';
        }
    });
}

function lazyLoadComponents() {
    // Lazy load non-critical components
    const lazyComponents = document.querySelectorAll('[data-lazy-load]');
    const componentObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const component = entry.target;
                const componentType = component.dataset.lazyLoad;
                
                // Load component based on type
                switch(componentType) {
                    case 'testimonial':
                        loadTestimonial(component);
                        break;
                    case 'feature':
                        loadFeature(component);
                        break;
                }
                
                observer.unobserve(component);
            }
        });
    });
    
    lazyComponents.forEach(comp => componentObserver.observe(comp));
}

function loadTestimonial(element) {
    // Placeholder for dynamic testimonial loading
    console.log('Loading testimonial component');
}

function loadFeature(element) {
    // Placeholder for dynamic feature loading
    console.log('Loading feature component');
}

// Analytics and tracking
function initAnalytics() {
    // Add event tracking for important user actions
    const trackableElements = document.querySelectorAll('[data-track]');
    trackableElements.forEach(element => {
        element.addEventListener('click', () => {
            const action = element.dataset.track;
            console.log(`Analytics: ${action} - ${element.textContent || element.href || element.innerText}`);
            
            // In a real implementation, you would send this to your analytics service
            // gtag('event', action, { ... });
        });
    });
}

// Initialize analytics
initAnalytics();

// Accessibility enhancements
function enhanceAccessibility() {
    // Add keyboard navigation improvements
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            // Close any open modals or dropdowns
            closeAllDropdowns();
        }
    });
    
    // Add ARIA labels for better screen reader support
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        if (!btn.getAttribute('aria-label')) {
            btn.setAttribute('aria-label', btn.textContent);
        }
    });
}

function closeAllDropdowns() {
    // Close any open dropdowns/menus
    const openDropdowns = document.querySelectorAll('.nav-menu[style*="flex"]');
    openDropdowns.forEach(dropdown => {
        dropdown.style.display = 'none';
    });
}

// Initialize accessibility enhancements
enhanceAccessibility();

console.log('Signature Extractor Landing Page loaded successfully with all interactive features!');