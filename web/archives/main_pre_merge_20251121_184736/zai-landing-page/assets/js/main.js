/**
 * Signature Extractor Landing Page - Main JavaScript
 * Handles navigation, scroll effects, and general interactions
 */

class SignatureExtractorLanding {
  constructor() {
    this.init();
  }

  init() {
    this.setupNavigation();
    this.setupScrollEffects();
    this.setupSmoothScrolling();
    this.setupMobileMenu();
    this.setupFeatureFilters();
    this.setupFeatureDetails();
    this.setupVideoModal();
    this.setupFormValidation();
    this.setupAnalytics();
  }

  /**
   * Setup navigation behavior
   */
  setupNavigation() {
    const navigation = document.querySelector('.navigation');
    const navLinks = document.querySelectorAll('.nav-link');

    // Handle scroll-based navigation styling
    this.handleNavigationScroll();
    window.addEventListener('scroll', () => this.handleNavigationScroll());

    // Handle active navigation link
    this.updateActiveNavLink();
    window.addEventListener('scroll', () => this.updateActiveNavLink());

    // Smooth scroll for navigation links
    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href');
        const targetSection = document.querySelector(targetId);

        if (targetSection) {
          const offsetTop = targetSection.offsetTop - 80; // Account for fixed navigation
          window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
          });
        }
      });
    });
  }

  /**
   * Handle navigation scroll effects
   */
  handleNavigationScroll() {
    const navigation = document.querySelector('.navigation');
    const scrolled = window.pageYOffset > 50;

    if (scrolled) {
      navigation.classList.add('scrolled');
    } else {
      navigation.classList.remove('scrolled');
    }
  }

  /**
   * Update active navigation link based on scroll position
   */
  updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    let currentSection = '';

    sections.forEach(section => {
      const sectionTop = section.offsetTop - 100;
      const sectionHeight = section.offsetHeight;

      if (window.pageYOffset >= sectionTop &&
          window.pageYOffset < sectionTop + sectionHeight) {
        currentSection = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentSection}`) {
        link.classList.add('active');
      }
    });
  }

  /**
   * Setup scroll-based animations
   */
  setupScrollEffects() {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');

          // Trigger stagger animation for children
          const staggerContainer = entry.target.querySelector('.stagger-animation');
          if (staggerContainer) {
            this.animateStaggerElements(staggerContainer);
          }
        }
      });
    }, observerOptions);

    // Observe elements with scroll animations
    const animatedElements = document.querySelectorAll('.animate-on-scroll, .animate-on-scroll-left, .animate-on-scroll-right, .animate-on-scroll-scale');
    animatedElements.forEach(element => {
      observer.observe(element);
    });

    // Observe feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
      observer.observe(card);
    });
  }

  /**
   * Animate staggered elements
   */
  animateStaggerElements(container) {
    const elements = container.querySelectorAll('*');
    elements.forEach((element, index) => {
      setTimeout(() => {
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
      }, index * 100);
    });
  }

  /**
   * Setup smooth scrolling
   */
  setupSmoothScrolling() {
    // Handle anchor links
    document.addEventListener('click', (e) => {
      const link = e.target.closest('a[href^="#"]');
      if (link && !link.classList.contains('nav-link')) {
        e.preventDefault();
        const targetId = link.getAttribute('href');
        const targetElement = document.querySelector(targetId);

        if (targetElement) {
          const offsetTop = targetElement.offsetTop - 80;
          window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
          });
        }
      }
    });
  }

  /**
   * Setup mobile menu
   */
  setupMobileMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navActions = document.querySelector('.nav-actions');

    if (!navToggle) return;

    navToggle.addEventListener('click', () => {
      const isOpen = navToggle.getAttribute('aria-expanded') === 'true';

      navToggle.setAttribute('aria-expanded', !isOpen);
      navToggle.classList.toggle('active');

      if (navMenu) navMenu.classList.toggle('active');
      if (navActions) navActions.classList.toggle('active');

      // Prevent body scroll when menu is open
      document.body.style.overflow = isOpen ? 'auto' : 'hidden';
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.navigation') &&
          navToggle.getAttribute('aria-expanded') === 'true') {
        navToggle.click();
      }
    });

    // Close menu when resizing to desktop
    window.addEventListener('resize', () => {
      if (window.innerWidth > 768 &&
          navToggle.getAttribute('aria-expanded') === 'true') {
        navToggle.click();
      }
    });
  }

  /**
   * Setup feature filters
   */
  setupFeatureFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const featureCards = document.querySelectorAll('.feature-card');

    if (!filterButtons.length) return;

    filterButtons.forEach(button => {
      button.addEventListener('click', () => {
        const filter = button.dataset.filter;

        // Update active button
        filterButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        // Filter feature cards
        featureCards.forEach(card => {
          const categories = card.dataset.categories?.split(',') || [];
          const shouldShow = filter === 'all' || categories.includes(filter);

          if (shouldShow) {
            card.style.display = 'block';
            setTimeout(() => {
              card.classList.remove('feature-card--filtered');
            }, 10);
          } else {
            card.classList.add('feature-card--filtered');
            setTimeout(() => {
              card.style.display = 'none';
            }, 300);
          }
        });
      });
    });
  }

  /**
   * Setup feature detail modals
   */
  setupFeatureDetails() {
    const learnMoreButtons = document.querySelectorAll('.feature-learn-more');

    learnMoreButtons.forEach(button => {
      button.addEventListener('click', () => {
        const card = button.closest('.feature-card');
        const title = card.querySelector('h3').textContent;
        const description = card.querySelector('p').textContent;

        this.openFeatureModal(title, description, button);
      });
    });
  }

  /**
   * Open feature detail modal
   */
  openFeatureModal(title, description, button) {
    const modal = document.createElement('div');
    modal.className = 'feature-modal';
    modal.innerHTML = `
      <div class="modal-backdrop"></div>
      <div class="modal-content">
        <div class="modal-header">
          <h3>${title}</h3>
          <button class="modal-close" aria-label="Close modal">×</button>
        </div>
        <div class="modal-body">
          <p>${description}</p>
          <div class="modal-features">
            <h4>Key Benefits</h4>
            <ul>
              <li>Increase productivity by 10x</li>
              <li>99.9% accuracy guaranteed</li>
              <li>Works with any document format</li>
              <li>Privacy-focused processing</li>
            </ul>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-primary modal-cta">Try This Feature</button>
          <button class="btn btn-secondary modal-close">Learn More</button>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    // Focus management
    const closeButtons = modal.querySelectorAll('.modal-close');
    const firstFocusable = modal.querySelector('.modal-cta');
    const lastFocusable = modal.querySelector('.modal-close:last-child');

    if (firstFocusable) firstFocusable.focus();

    // Close modal handlers
    const closeModal = () => {
      modal.classList.add('closing');
      setTimeout(() => {
        document.body.removeChild(modal);
        button.focus();
      }, 300);
    };

    closeButtons.forEach(btn => {
      btn.addEventListener('click', closeModal);
    });

    modal.querySelector('.modal-backdrop').addEventListener('click', closeModal);

    // Escape key to close
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        closeModal();
        document.removeEventListener('keydown', handleEscape);
      }
    };
    document.addEventListener('keydown', handleEscape);

    // Focus trap
    const handleTabKey = (e) => {
      if (e.key === 'Tab') {
        if (e.shiftKey) {
          if (document.activeElement === firstFocusable) {
            e.preventDefault();
            lastFocusable.focus();
          }
        } else {
          if (document.activeElement === lastFocusable) {
            e.preventDefault();
            firstFocusable.focus();
          }
        }
      }
    };
    modal.addEventListener('keydown', handleTabKey);

    // CTA button handler
    modal.querySelector('.modal-cta').addEventListener('click', () => {
      this.trackEvent('feature_cta_clicked', { feature: title });
      window.location.href = '#download';
    });

    // Animate modal appearance
    requestAnimationFrame(() => {
      modal.classList.add('active');
    });
  }

  /**
   * Setup video modal
   */
  setupVideoModal() {
    const videoTriggers = document.querySelectorAll('.video-trigger');

    videoTriggers.forEach(trigger => {
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        this.openVideoModal();
      });
    });
  }

  /**
   * Open video modal
   */
  openVideoModal() {
    const modal = document.createElement('div');
    modal.className = 'video-modal';
    modal.innerHTML = `
      <div class="modal-backdrop"></div>
      <div class="modal-content">
        <div class="modal-header">
          <h3>Product Demo</h3>
          <button class="modal-close" aria-label="Close video">×</button>
        </div>
        <div class="modal-body">
          <div class="video-container">
            <iframe
              src="https://www.youtube.com/embed/dQw4w9WgXcQ"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen>
            </iframe>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    // Close modal handlers
    const closeModal = () => {
      const iframe = modal.querySelector('iframe');
      iframe.src = iframe.src; // Stop video playback

      modal.classList.add('closing');
      setTimeout(() => {
        document.body.removeChild(modal);
      }, 300);
    };

    const closeButtons = modal.querySelectorAll('.modal-close');
    closeButtons.forEach(btn => {
      btn.addEventListener('click', closeModal);
    });

    modal.querySelector('.modal-backdrop').addEventListener('click', closeModal);

    // Animate modal appearance
    requestAnimationFrame(() => {
      modal.classList.add('active');
    });

    this.trackEvent('video_modal_opened');
  }

  /**
   * Setup form validation
   */
  setupFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');

    forms.forEach(form => {
      form.addEventListener('submit', (e) => {
        if (!this.validateForm(form)) {
          e.preventDefault();
        }
      });

      // Real-time validation
      const inputs = form.querySelectorAll('input, textarea, select');
      inputs.forEach(input => {
        input.addEventListener('blur', () => {
          this.validateField(input);
        });

        input.addEventListener('input', () => {
          if (input.classList.contains('error')) {
            this.validateField(input);
          }
        });
      });
    });
  }

  /**
   * Validate form
   */
  validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
      if (!this.validateField(input)) {
        isValid = false;
      }
    });

    return isValid;
  }

  /**
   * Validate individual field
   */
  validateField(field) {
    const value = field.value.trim();
    const fieldType = field.type;
    let isValid = true;
    let errorMessage = '';

    // Remove previous error states
    field.classList.remove('error');
    const errorElement = field.parentNode.querySelector('.error-message');
    if (errorElement) {
      errorElement.remove();
    }

    // Validation rules
    if (!value) {
      isValid = false;
      errorMessage = 'This field is required';
    } else if (fieldType === 'email') {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(value)) {
        isValid = false;
        errorMessage = 'Please enter a valid email address';
      }
    } else if (fieldType === 'tel') {
      const phoneRegex = /^[\d\s\-\+\(\)]+$/;
      if (!phoneRegex.test(value)) {
        isValid = false;
        errorMessage = 'Please enter a valid phone number';
      }
    }

    // Show error if invalid
    if (!isValid) {
      field.classList.add('error');

      const errorElement = document.createElement('div');
      errorElement.className = 'error-message';
      errorElement.textContent = errorMessage;
      field.parentNode.appendChild(errorElement);
    }

    return isValid;
  }

  /**
   * Setup analytics tracking
   */
  setupAnalytics() {
    // Track page view
    this.trackEvent('page_view', {
      page: window.location.pathname,
      title: document.title
    });

    // Track button clicks
    const trackingButtons = document.querySelectorAll('[data-track]');
    trackingButtons.forEach(button => {
      button.addEventListener('click', () => {
        const eventName = button.dataset.track;
        const eventData = JSON.parse(button.dataset.trackData || '{}');
        this.trackEvent(eventName, eventData);
      });
    });

    // Track scroll depth
    this.trackScrollDepth();
  }

  /**
   * Track analytics events
   */
  trackEvent(eventName, data = {}) {
    // Google Analytics 4
    if (typeof gtag !== 'undefined') {
      gtag('event', eventName, {
        custom_map: data
      });
    }

    // Custom analytics (placeholder)
    console.log('Analytics Event:', eventName, data);

    // You could send to your own analytics endpoint here
    // fetch('/api/analytics', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ event: eventName, data, timestamp: Date.now() })
    // });
  }

  /**
   * Track scroll depth
   */
  trackScrollDepth() {
    const depths = [25, 50, 75, 90];
    const tracked = new Set();

    const checkScrollDepth = () => {
      const scrollPercent = Math.round(
        (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100
      );

      depths.forEach(depth => {
        if (scrollPercent >= depth && !tracked.has(depth)) {
          tracked.add(depth);
          this.trackEvent('scroll_depth', { depth: scrollPercent });
        }
      });
    };

    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          checkScrollDepth();
          ticking = false;
        });
        ticking = true;
      }
    });
  }

  /**
   * Utility: Debounce function
   */
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  /**
   * Utility: Throttle function
   */
  throttle(func, limit) {
    let inThrottle;
    return function(...args) {
      if (!inThrottle) {
        func.apply(this, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  }

  /**
   * Cleanup method
   */
  destroy() {
    // Remove event listeners and cleanup
    window.removeEventListener('scroll', this.handleNavigationScroll);
    window.removeEventListener('scroll', this.updateActiveNavLink);
    // ... other cleanup
  }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
  window.signatureExtractorLanding = new SignatureExtractorLanding();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    // Pause animations when page is not visible
    document.body.classList.add('page-hidden');
  } else {
    // Resume animations when page becomes visible
    document.body.classList.remove('page-hidden');
  }
});

// Handle window resize with debouncing
let resizeTimeout;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    // Trigger any resize-dependent logic
    window.dispatchEvent(new CustomEvent('app-resize'));
  }, 250);
});

// Export for potential use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SignatureExtractorLanding;
}