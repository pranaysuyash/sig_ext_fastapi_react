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

  window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    // Add shadow on scroll
    if (currentScroll > 10) {
      navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
    } else {
      navbar.style.boxShadow = 'none';
    }

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
    stopAutoPlay();
    autoPlayInterval = setInterval(nextStep, 3000);
  }

  function stopAutoPlay() {
    if (autoPlayInterval) {
      clearInterval(autoPlayInterval);
    }
  }

  // Dot click handlers
  dots.forEach((dot) => {
    dot.addEventListener('click', () => {
      const stepNumber = parseInt(dot.dataset.step, 10);
      showStep(stepNumber);
      stopAutoPlay();
      // Restart autoplay after user interaction
      setTimeout(startAutoPlay, 3000);
    });
  });

  // Start autoplay
  if (steps.length > 0) {
    startAutoPlay();
  }

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
  const CTA_FALLBACK_URL = 'https://pranaysuyash.gumroad.com/l/signkit-v1';
  const ctaButtons = [
    document.getElementById('navCTA'),
    document.getElementById('heroCTA'),
    document.getElementById('pricingCTA'),
    document.getElementById('finalCTA'),
    document.getElementById('demoBtn'),
  ];

  ctaButtons.forEach((button) => {
    if (!button) return;

    button.addEventListener('click', (e) => {
      if (button.id === 'demoBtn') {
        const demoSection = document.getElementById('demo');
        if (demoSection) {
          demoSection.scrollIntoView({ behavior: 'smooth' });
        }
      } else {
        const dataHref = button.getAttribute('data-href');
        const anchorHref = button.getAttribute('href');

        if (dataHref) {
          // Analytics helper will intercept these clicks to append UTMs + open Gumroad
          return;
        } else if (anchorHref && anchorHref !== '#') {
          // Allow native anchor navigation
          return;
        } else {
          window.open(CTA_FALLBACK_URL, '_blank');
        }
      }

      createRipple(e, button);
    });
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
