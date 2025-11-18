// ============================================
// Main JavaScript for Signature Extractor Landing Page
// ============================================

document.addEventListener('DOMContentLoaded', () => {
  // Initialize all features
  initNavigation();
  initProgressBar();
  initDemoCarousel();
  initTabs();
  initFAQ();
  initBackToTop();
  initCTAButtons();
  initScrollAnimations();
});

// ============================================
// Navigation
// ============================================
function initNavigation() {
  const navbar = document.getElementById('navbar');
  const navToggle = document.getElementById('navToggle');
  let lastScroll = 0;

  // Navbar scroll effect
  window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    // Add shadow on scroll
    if (currentScroll > 10) {
      navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
    } else {
      navbar.style.boxShadow = 'none';
    }

    lastScroll = currentScroll;
  });

  // Mobile menu toggle
  if (navToggle) {
    navToggle.addEventListener('click', () => {
      navToggle.classList.toggle('active');
      // Add mobile menu functionality here if needed
    });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        const offsetTop = target.offsetTop - 72; // Account for fixed navbar
        window.scrollTo({
          top: offsetTop,
          behavior: 'smooth',
        });
      }
    });
  });
}

// ============================================
// Progress Bar
// ============================================
function initProgressBar() {
  const progressBar = document.getElementById('progressBar');

  window.addEventListener('scroll', () => {
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    const scrollPercentage =
      (scrollTop / (documentHeight - windowHeight)) * 100;

    progressBar.style.width = `${Math.min(scrollPercentage, 100)}%`;
  });
}

// ============================================
// Demo Carousel
// ============================================
function initDemoCarousel() {
  const dots = document.querySelectorAll('.demo-dot');
  const steps = document.querySelectorAll('.demo-step');
  let currentStep = 1;
  let autoPlayInterval;

  function showStep(stepNumber) {
    // Remove active class from all
    steps.forEach((step) => step.classList.remove('active'));
    dots.forEach((dot) => dot.classList.remove('active'));

    // Add active class to current
    const currentStepEl = document.querySelector(
      `.demo-step[data-step="${stepNumber}"]`
    );
    const currentDotEl = document.querySelector(
      `.demo-dot[data-step="${stepNumber}"]`
    );

    if (currentStepEl) currentStepEl.classList.add('active');
    if (currentDotEl) currentDotEl.classList.add('active');

    currentStep = stepNumber;
  }

  function nextStep() {
    const next = currentStep >= steps.length ? 1 : currentStep + 1;
    showStep(next);
  }

  function startAutoPlay() {
    autoPlayInterval = setInterval(nextStep, 5000);
  }

  function stopAutoPlay() {
    if (autoPlayInterval) {
      clearInterval(autoPlayInterval);
    }
  }

  // Dot click handlers
  dots.forEach((dot) => {
    dot.addEventListener('click', () => {
      const stepNumber = parseInt(dot.dataset.step);
      showStep(stepNumber);
      stopAutoPlay();
      // Restart autoplay after user interaction
      setTimeout(startAutoPlay, 5000);
    });
  });

  // Start autoplay
  startAutoPlay();

  // Pause on hover
  const demoWindow = document.querySelector('.demo-window');
  if (demoWindow) {
    demoWindow.addEventListener('mouseenter', stopAutoPlay);
    demoWindow.addEventListener('mouseleave', startAutoPlay);
  }
}

// ============================================
// Tabs (Solution Section)
// ============================================
function initTabs() {
  const tabButtons = document.querySelectorAll('.tab-button');
  const tabContents = document.querySelectorAll('.tab-content');

  function showTab(tabId) {
    // Remove active from all
    tabButtons.forEach((btn) => btn.classList.remove('active'));
    tabContents.forEach((content) => content.classList.remove('active'));

    // Add active to selected
    const selectedButton = document.querySelector(
      `.tab-button[data-tab="${tabId}"]`
    );
    const selectedContent = document.getElementById(`tab-${tabId}`);

    if (selectedButton) selectedButton.classList.add('active');
    if (selectedContent) selectedContent.classList.add('active');
  }

  tabButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const tabId = button.dataset.tab;
      showTab(tabId);
    });
  });

  // Show first tab by default
  if (tabButtons.length > 0) {
    showTab(tabButtons[0].dataset.tab);
  }
}

// ============================================
// FAQ Accordion
// ============================================
function initFAQ() {
  const faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach((item) => {
    const question = item.querySelector('.faq-question');

    question.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');

      // Close all items
      faqItems.forEach((otherItem) => {
        otherItem.classList.remove('open');
      });

      // Toggle current item
      if (!isOpen) {
        item.classList.add('open');
      }
    });
  });
}

// ============================================
// Back to Top Button
// ============================================
function initBackToTop() {
  const backToTopButton = document.getElementById('backToTop');

  if (!backToTopButton) return;

  // Show/hide button based on scroll position
  window.addEventListener('scroll', () => {
    if (window.pageYOffset > 500) {
      backToTopButton.classList.add('visible');
    } else {
      backToTopButton.classList.remove('visible');
    }
  });

  // Scroll to top on click
  backToTopButton.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  });
}

// ============================================
// CTA Buttons
// ============================================
function initCTAButtons() {
  const ctaButtons = [
    document.getElementById('navCTA'),
    document.getElementById('heroCTA'),
    document.getElementById('pricingCTA'),
    document.getElementById('finalCTA'),
    document.getElementById('demoBtn'),
  ];

  ctaButtons.forEach((button) => {
    if (button) {
      button.addEventListener('click', (e) => {
        // Handle CTA click
        if (button.id === 'demoBtn') {
          // Scroll to demo or open modal
          const demoSection = document.getElementById('demo');
          if (demoSection) {
            demoSection.scrollIntoView({ behavior: 'smooth' });
          } else {
            // Or show a demo modal
            console.log('Show demo modal');
          }
        } else {
          // Handle purchase CTAs
          console.log('Purchase CTA clicked:', button.id);
          // Add your purchase flow here
          alert(
            'Thank you for your interest! Purchase flow would be integrated here.'
          );
        }

        // Add ripple effect
        createRipple(e, button);
      });
    }
  });
}

// ============================================
// Ripple Effect
// ============================================
function createRipple(event, button) {
  const circle = document.createElement('span');
  const diameter = Math.max(button.clientWidth, button.clientHeight);
  const radius = diameter / 2;

  const rect = button.getBoundingClientRect();
  circle.style.width = circle.style.height = `${diameter}px`;
  circle.style.left = `${event.clientX - rect.left - radius}px`;
  circle.style.top = `${event.clientY - rect.top - radius}px`;
  circle.classList.add('ripple');

  // Add styles for ripple
  circle.style.position = 'absolute';
  circle.style.borderRadius = '50%';
  circle.style.background = 'rgba(255, 255, 255, 0.6)';
  circle.style.transform = 'scale(0)';
  circle.style.animation = 'ripple-animation 0.6s ease-out';
  circle.style.pointerEvents = 'none';

  // Ensure button is positioned
  if (getComputedStyle(button).position === 'static') {
    button.style.position = 'relative';
  }

  // Ensure button has overflow hidden
  button.style.overflow = 'hidden';

  button.appendChild(circle);

  setTimeout(() => {
    circle.remove();
  }, 600);
}

// Add ripple animation to stylesheet
const style = document.createElement('style');
style.innerHTML = `
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ============================================
// Scroll Animations
// ============================================
function initScrollAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px',
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        // Optionally unobserve after animation
        // observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Observe all elements with .animate-on-scroll class
  document.querySelectorAll('.animate-on-scroll').forEach((el) => {
    observer.observe(el);
  });
}

// ============================================
// Utility Functions
// ============================================

// Debounce function for performance
function debounce(func, wait) {
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

// Check if element is in viewport
function isInViewport(element) {
  const rect = element.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <=
      (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

// Get scroll percentage
function getScrollPercentage() {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  const scrollHeight =
    document.documentElement.scrollHeight -
    document.documentElement.clientHeight;
  return (scrollTop / scrollHeight) * 100;
}

// ============================================
// Console Art
// ============================================
console.log(
  '%cSignature Extractor',
  'font-size: 24px; font-weight: bold; color: #3b82f6;'
);
console.log(
  '%cBuilt with care for professionals who need precision and privacy.',
  'font-size: 12px; color: #6b7280;'
);
console.log(
  '%cInterested in how this was built? Check out the code!',
  'font-size: 12px; color: #10b981;'
);
