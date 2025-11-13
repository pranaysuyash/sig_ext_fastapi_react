/**
 * Signature Extractor - Main Application Controller
 * Advanced landing page with sophisticated interactions and animations
 */

class SignatureExtractorLanding {
  constructor() {
    console.log('🚀 Signature Extractor Landing - Initializing...');

    this.components = {};
    this.isLoaded = false;
    this.performanceMode = 'auto'; // 'high', 'medium', 'low', 'auto'
    this.reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    this.touchDevice = 'ontouchstart' in window;
    this.scrollY = 0;
    this.mousePos = { x: 0, y: 0 };
    this.viewport = {
      width: window.innerWidth,
      height: window.innerHeight
    };

    // Performance monitoring
    this.performance = {
      fps: 60,
      frameTime: 0,
      lastFrameTime: performance.now(),
      adaptiveQuality: true
    };

    this.init();
  }

  init() {
    this.setupLoadingScreen();
    this.bindGlobalEvents();
    this.detectCapabilities();
    this.initializeComponents();
    this.setupPerformanceMonitoring();
    this.setupAnalytics();
  }

  setupLoadingScreen() {
    console.log('📺 Setting up loading screen...');
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
      console.log('✅ Loading screen found, starting animation');
      // Start loading animation
      loadingScreen.classList.add('loading');

      // Simulate loading process
      setTimeout(() => {
        console.log('⏰ Loading complete, transitioning to main content');
        this.completeLoading();
      }, 2000);
    } else {
      console.log('❌ Loading screen not found, skipping directly to main content');
      this.completeLoading();
    }
  }

  completeLoading() {
    console.log('🎯 Completing loading sequence...');
    const loadingScreen = document.getElementById('loading-screen');
    const body = document.body;

    if (loadingScreen) {
      loadingScreen.classList.add('hidden');
      console.log('🔄 Added hidden class to loading screen');

      setTimeout(() => {
        loadingScreen.style.display = 'none';
        body.classList.remove('loading');
        console.log('✨ Loading screen hidden, body loading class removed');
        this.startMainAnimations();
      }, 500);
    } else {
      body.classList.remove('loading');
      this.startMainAnimations();
    }

    this.isLoaded = true;
    this.triggerEvent('app:loaded');
    console.log('🎉 App fully loaded!');
  }

  startMainAnimations() {
    // Trigger entrance animations
    this.animateOnScroll();

    // Start particle systems
    if (window.heroParticleSystem) {
      window.heroParticleSystem.start();
    }

    // Initialize interactive components
    this.initializeInteractions();
  }

  bindGlobalEvents() {
    // Scroll events
    window.addEventListener('scroll', this.throttle(() => {
      this.scrollY = window.pageYOffset;
      this.handleScroll();
    }, 16)); // 60fps

    // Resize events
    window.addEventListener('resize', this.debounce(() => {
      this.handleResize();
    }, 250));

    // Mouse events
    document.addEventListener('mousemove', (e) => {
      this.mousePos.x = e.clientX;
      this.mousePos.y = e.clientY;
      this.handleMouseMove(e);
    });

    // Keyboard events
    document.addEventListener('keydown', (e) => {
      this.handleKeyboard(e);
    });

    // Visibility change
    document.addEventListener('visibilitychange', () => {
      this.handleVisibilityChange();
    });

    // Touch events
    if (this.touchDevice) {
      this.setupTouchEvents();
    }

    // Performance monitoring
    if (this.performance.adaptiveQuality) {
      this.monitorFrameRate();
    }
  }

  detectCapabilities() {
    // Detect browser capabilities
    this.capabilities = {
      webgl: this.detectWebGL(),
      webp: this.detectWebP(),
      intersectionObserver: 'IntersectionObserver' in window,
      passiveListeners: this.detectPassiveListeners(),
      devicePixelRatio: window.devicePixelRatio || 1,
      memory: navigator.deviceMemory || 4,
      cores: navigator.hardwareConcurrency || 4
    };

    // Determine performance mode
    this.determinePerformanceMode();
  }

  detectWebGL() {
    try {
      const canvas = document.createElement('canvas');
      return !!(window.WebGLRenderingContext &&
        (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
    } catch (e) {
      return false;
    }
  }

  detectWebP() {
    const canvas = document.createElement('canvas');
    return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
  }

  detectPassiveListeners() {
    let supportsPassive = false;
    try {
      const opts = Object.defineProperty({}, 'passive', {
        get: () => {
          supportsPassive = true;
          return false;
        }
      });
      window.addEventListener('testPassive', null, opts);
      window.removeEventListener('testPassive', null, opts);
    } catch (e) {
      supportsPassive = false;
    }
    return supportsPassive;
  }

  determinePerformanceMode() {
    const { memory, cores, devicePixelRatio } = this.capabilities;

    if (this.reducedMotion) {
      this.performanceMode = 'low';
    } else if (memory >= 8 && cores >= 8 && devicePixelRatio <= 2) {
      this.performanceMode = 'high';
    } else if (memory >= 4 && cores >= 4) {
      this.performanceMode = 'medium';
    } else {
      this.performanceMode = 'low';
    }

    console.log(`Performance mode: ${this.performanceMode}`);
  }

  initializeComponents() {
    // Initialize navigation
    this.initializeNavigation();

    // Initialize smooth scrolling
    this.initializeSmoothScrolling();

    // Initialize scroll animations
    this.initializeScrollAnimations();

    // Initialize mobile menu
    if (this.touchDevice) {
      this.initializeMobileMenu();
    }

    // Initialize feature filters
    this.initializeFeatureFilters();

    // Initialize video modal
    this.initializeVideoModal();

    // Initialize form validation
    this.initializeFormValidation();

    // Initialize theme toggle
    this.initializeThemeToggle();
  }

  initializeNavigation() {
    const navigation = document.querySelector('.navigation');
    if (!navigation) return;

    // Sticky navigation with backdrop blur
    this.setupStickyNavigation(navigation);

    // Active state management
    this.setupNavigationActiveStates();

    // Mobile navigation
    this.setupMobileNavigation();
  }

  setupStickyNavigation(navigation) {
    const navHeight = navigation.offsetHeight;
    let lastScrollY = this.scrollY;
    let ticking = false;

    const updateNavigation = () => {
      if (this.scrollY > navHeight) {
        navigation.classList.add('scrolled');

        // Hide/show on scroll
        if (this.scrollY > lastScrollY && this.scrollY > navHeight * 2) {
          navigation.classList.add('hidden');
        } else {
          navigation.classList.remove('hidden');
        }
      } else {
        navigation.classList.remove('scrolled', 'hidden');
      }

      lastScrollY = this.scrollY;
      ticking = false;
    };

    const requestTick = () => {
      if (!ticking) {
        requestAnimationFrame(updateNavigation);
        ticking = true;
      }
    };

    // Initial check
    updateNavigation();
  }

  setupNavigationActiveStates() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    const updateActiveStates = () => {
      const scrollPos = this.scrollY + 100;

      sections.forEach(section => {
        const top = section.offsetTop;
        const height = section.offsetHeight;
        const id = section.getAttribute('id');

        if (scrollPos >= top && scrollPos < top + height) {
          navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${id}`) {
              link.classList.add('active');
            }
          });
        }
      });
    };

    this.throttledUpdateActiveStates = this.throttle(updateActiveStates, 100);
    window.addEventListener('scroll', this.throttledUpdateActiveStates);
  }

  setupMobileNavigation() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navOverlay = document.querySelector('.nav-overlay');

    if (!navToggle || !navMenu) return;

    const toggleMobileMenu = () => {
      const isOpen = navToggle.classList.contains('active');

      navToggle.classList.toggle('active');
      navMenu.classList.toggle('active');
      document.body.classList.toggle('nav-open');

      // Prevent scroll when menu is open
      document.body.style.overflow = isOpen ? '' : 'hidden';

      // Toggle overlay
      if (navOverlay) {
        navOverlay.classList.toggle('active');
      }

      // Update ARIA attributes
      navToggle.setAttribute('aria-expanded', !isOpen);
    };

    navToggle.addEventListener('click', toggleMobileMenu);

    // Close menu on overlay click
    if (navOverlay) {
      navOverlay.addEventListener('click', toggleMobileMenu);
    }

    // Close menu on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navToggle.classList.contains('active')) {
        toggleMobileMenu();
      }
    });

    // Close menu on nav link click
    const mobileNavLinks = navMenu.querySelectorAll('.nav-link');
    mobileNavLinks.forEach(link => {
      link.addEventListener('click', () => {
        if (navToggle.classList.contains('active')) {
          toggleMobileMenu();
        }
      });
    });
  }

  initializeSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        const target = document.querySelector(href);

        if (target) {
          e.preventDefault();

          const navHeight = document.querySelector('.navigation')?.offsetHeight || 0;
          const targetY = target.offsetTop - navHeight - 20;

          // Smooth scroll
          window.scrollTo({
            top: targetY,
            behavior: 'smooth'
          });

          // Update URL without reload
          history.pushState(null, null, href);

          // Update focus for accessibility
          target.setAttribute('tabindex', '-1');
          target.focus();
        }
      });
    });
  }

  initializeScrollAnimations() {
    if (!this.capabilities.intersectionObserver || this.reducedMotion) return;

    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.animateElement(entry.target);
        }
      });
    }, observerOptions);

    // Observe elements with animation classes
    const animatedElements = document.querySelectorAll('.animate-on-scroll, .feature-card, .workflow-step, .testimonial-card');
    animatedElements.forEach(el => {
      observer.observe(el);
    });

    this.scrollObserver = observer;
  }

  animateElement(element) {
    // Add animation classes based on element type
    if (element.classList.contains('feature-card')) {
      element.style.animation = 'fadeInUp 0.6s ease-out forwards';
    } else if (element.classList.contains('workflow-step')) {
      element.style.animation = 'fadeInUp 0.8s ease-out forwards';
    } else if (element.classList.contains('testimonial-card')) {
      element.style.animation = 'fadeInUp 0.7s ease-out forwards';
    } else {
      element.classList.add('is-visible');
    }
  }

  initializeMobileMenu() {
    // Mobile-specific enhancements
    if (this.touchDevice) {
      document.body.classList.add('touch-device');
    }
  }

  initializeFeatureFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const featureCards = document.querySelectorAll('.feature-card');

    if (!filterButtons.length || !featureCards.length) return;

    filterButtons.forEach(button => {
      button.addEventListener('click', () => {
        const category = button.getAttribute('data-category');

        // Update active button
        filterButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        // Filter cards
        featureCards.forEach(card => {
          const cardCategories = card.getAttribute('data-categories')?.split(',') || [];

          if (category === 'all' || cardCategories.includes(category)) {
            card.style.display = '';
            card.style.animation = 'fadeInUp 0.5s ease-out forwards';
          } else {
            card.style.display = 'none';
          }
        });

        // Announce filter change
        this.announceFilterChange(category);
      });
    });
  }

  initializeVideoModal() {
    const videoButtons = document.querySelectorAll('[data-video-modal]');
    const modal = document.getElementById('video-modal');
    const closeButton = modal?.querySelector('.modal-close');
    const videoPlayer = modal?.querySelector('video');

    if (!videoButtons.length || !modal) return;

    const openModal = (videoUrl) => {
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';

      if (videoPlayer && videoUrl) {
        videoPlayer.src = videoUrl;
        videoPlayer.play();
      }

      // Focus management
      modal.setAttribute('aria-hidden', 'false');
      closeButton?.focus();
    };

    const closeModal = () => {
      modal.classList.remove('active');
      document.body.style.overflow = '';

      if (videoPlayer) {
        videoPlayer.pause();
        videoPlayer.src = '';
      }

      modal.setAttribute('aria-hidden', 'true');
    };

    videoButtons.forEach(button => {
      button.addEventListener('click', () => {
        const videoUrl = button.getAttribute('data-video-url');
        openModal(videoUrl);
      });
    });

    closeButton?.addEventListener('click', closeModal);

    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal();
      }
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('active')) {
        closeModal();
      }
    });
  }

  initializeFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');

    forms.forEach(form => {
      const submitButton = form.querySelector('button[type="submit"]');
      const inputs = form.querySelectorAll('input, textarea, select');

      const validateForm = () => {
        let isValid = true;

        inputs.forEach(input => {
          const isFieldValid = this.validateField(input);
          if (!isFieldValid) {
            isValid = false;
          }
        });

        if (submitButton) {
          submitButton.disabled = !isValid;
        }

        return isValid;
      };

      inputs.forEach(input => {
        input.addEventListener('blur', () => this.validateField(input));
        input.addEventListener('input', validateForm);
      });

      form.addEventListener('submit', (e) => {
        if (!validateForm()) {
          e.preventDefault();
          this.showFormError(form);
        }
      });
    });
  }

  validateField(field) {
    const value = field.value.trim();
    const required = field.hasAttribute('required');
    const type = field.getAttribute('type');
    const pattern = field.getAttribute('pattern');

    let isValid = true;
    let errorMessage = '';

    // Required validation
    if (required && !value) {
      isValid = false;
      errorMessage = 'This field is required';
    }

    // Email validation
    if (isValid && type === 'email' && value) {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(value)) {
        isValid = false;
        errorMessage = 'Please enter a valid email address';
      }
    }

    // Pattern validation
    if (isValid && pattern && value) {
      const regex = new RegExp(pattern);
      if (!regex.test(value)) {
        isValid = false;
        errorMessage = field.getAttribute('data-error-message') || 'Please enter a valid value';
      }
    }

    // Update UI
    this.updateFieldValidation(field, isValid, errorMessage);

    return isValid;
  }

  updateFieldValidation(field, isValid, errorMessage) {
    const formGroup = field.closest('.form-group');
    if (!formGroup) return;

    const errorElement = formGroup.querySelector('.field-error');

    field.classList.toggle('invalid', !isValid);
    field.classList.toggle('valid', isValid);

    if (errorElement) {
      errorElement.textContent = errorMessage;
      errorElement.style.display = errorMessage ? 'block' : 'none';
    }
  }

  showFormError(form) {
    const errorSummary = form.querySelector('.form-error-summary');
    if (errorSummary) {
      errorSummary.style.display = 'block';
      errorSummary.focus();
    }
  }

  initializeThemeToggle() {
    const themeToggle = document.querySelector('.theme-toggle');
    if (!themeToggle) return;

    const currentTheme = localStorage.getItem('theme') || 'dark';
    this.setTheme(currentTheme);

    themeToggle.addEventListener('click', () => {
      const newTheme = document.body.classList.contains('light-theme') ? 'dark' : 'light';
      this.setTheme(newTheme);
      localStorage.setItem('theme', newTheme);
    });
  }

  setTheme(theme) {
    document.body.classList.toggle('light-theme', theme === 'light');
    document.body.classList.toggle('dark-theme', theme === 'dark');

    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
      themeToggle.setAttribute('aria-label', `Switch to ${theme === 'light' ? 'dark' : 'light'} theme`);
    }
  }

  initializeInteractions() {
    // Hover effects for cards
    this.setupCardInteractions();

    // Parallax effects
    if (this.performanceMode !== 'low') {
      this.setupParallaxEffects();
    }

    // Micro-interactions
    this.setupMicroInteractions();
  }

  setupCardInteractions() {
    const cards = document.querySelectorAll('.feature-card, .pricing-card, .testimonial-card');

    cards.forEach(card => {
      card.addEventListener('mouseenter', (e) => {
        this.handleCardHover(e, true);
      });

      card.addEventListener('mouseleave', (e) => {
        this.handleCardHover(e, false);
      });

      card.addEventListener('mousemove', (e) => {
        this.handleCardMouseMove(e);
      });
    });
  }

  handleCardHover(e, isEntering) {
    const card = e.currentTarget;

    if (isEntering) {
      card.classList.add('hovered');

      // Add subtle glow effect
      card.style.boxShadow = '0 10px 40px rgba(0, 255, 136, 0.2)';
    } else {
      card.classList.remove('hovered');
      card.style.boxShadow = '';
      card.style.transform = '';
    }
  }

  handleCardMouseMove(e) {
    const card = e.currentTarget;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const angleX = (y - centerY) / centerY * 5;
    const angleY = (centerX - x) / centerX * 5;

    card.style.transform = `perspective(1000px) rotateX(${angleX}deg) rotateY(${angleY}deg) translateZ(10px)`;
  }

  setupParallaxEffects() {
    const parallaxElements = document.querySelectorAll('[data-parallax]');

    const updateParallax = () => {
      const scrolled = this.scrollY;

      parallaxElements.forEach(element => {
        const speed = parseFloat(element.getAttribute('data-parallax')) || 0.5;
        const yPos = -(scrolled * speed);

        element.style.transform = `translateY(${yPos}px)`;
      });
    };

    this.throttledParallax = this.throttle(updateParallax, 16);
    window.addEventListener('scroll', this.throttledParallax);
  }

  setupMicroInteractions() {
    // Button ripple effects
    this.setupRippleEffects();

    // Input focus effects
    this.setupInputEffects();

    // Link hover effects
    this.setupLinkEffects();
  }

  setupRippleEffects() {
    const buttons = document.querySelectorAll('.btn');

    buttons.forEach(button => {
      button.addEventListener('click', (e) => {
        this.createRipple(e, button);
      });
    });
  }

  createRipple(e, button) {
    const ripple = document.createElement('span');
    ripple.className = 'ripple';

    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    ripple.style.cssText = `
      width: ${size}px;
      height: ${size}px;
      left: ${x}px;
      top: ${y}px;
    `;

    button.appendChild(ripple);

    setTimeout(() => {
      ripple.remove();
    }, 600);
  }

  setupInputEffects() {
    const inputs = document.querySelectorAll('input, textarea');

    inputs.forEach(input => {
      input.addEventListener('focus', () => {
        input.parentElement?.classList.add('focused');
      });

      input.addEventListener('blur', () => {
        if (!input.value) {
          input.parentElement?.classList.remove('focused');
        }
      });
    });
  }

  setupLinkEffects() {
    const links = document.querySelectorAll('a:not(.btn)');

    links.forEach(link => {
      link.addEventListener('mouseenter', () => {
        link.style.transform = 'translateX(2px)';
      });

      link.addEventListener('mouseleave', () => {
        link.style.transform = '';
      });
    });
  }

  setupTouchEvents() {
    // Touch-specific optimizations
    let touchStartY = 0;
    let touchEndY = 0;

    document.addEventListener('touchstart', (e) => {
      touchStartY = e.touches[0].clientY;
    });

    document.addEventListener('touchend', (e) => {
      touchEndY = e.changedTouches[0].clientY;
      this.handleSwipe(touchStartY, touchEndY);
    });
  }

  handleSwipe(startY, endY) {
    const diff = startY - endY;
    const threshold = 50;

    if (Math.abs(diff) > threshold) {
      if (diff > 0) {
        // Swipe up
        this.triggerEvent('swipe:up');
      } else {
        // Swipe down
        this.triggerEvent('swipe:down');
      }
    }
  }

  handleScroll() {
    // Update scroll-based animations
    this.animateOnScroll();

    // Update navigation
    if (this.throttledUpdateActiveStates) {
      this.throttledUpdateActiveStates();
    }
  }

  handleResize() {
    this.viewport = {
      width: window.innerWidth,
      height: window.innerHeight
    };

    // Update component sizes
    this.updateComponentSizes();

    // Reinitialize particle systems if needed
    if (window.heroParticleSystem) {
      window.heroParticleSystem.updateBounds();
    }
  }

  handleMouseMove(e) {
    // Mouse-based effects
    if (this.performanceMode !== 'low') {
      this.updateMouseEffects(e);
    }
  }

  handleKeyboard(e) {
    // Keyboard shortcuts
    if (e.key === '/' && e.ctrlKey) {
      e.preventDefault();
      this.focusSearch();
    }
  }

  handleVisibilityChange() {
    if (document.hidden) {
      // Pause animations when tab is not visible
      this.pauseAnimations();
    } else {
      // Resume animations when tab becomes visible
      this.resumeAnimations();
    }
  }

  updateMouseEffects(e) {
    // Update mouse-following effects
    const mouseX = e.clientX;
    const mouseY = e.clientY;

    // Update any mouse-following elements
    const mouseFollowers = document.querySelectorAll('[data-mouse-follow]');
    mouseFollowers.forEach(element => {
      element.style.transform = `translate(${mouseX}px, ${mouseY}px)`;
    });
  }

  updateComponentSizes() {
    // Update any size-dependent components
    const workflowContainer = document.getElementById('workflow-container');
    if (workflowContainer && window.interactiveWorkflow) {
      window.interactiveWorkflow.handleResize();
    }
  }

  animateOnScroll() {
    // Trigger scroll-based animations
    const scrollElements = document.querySelectorAll('[data-scroll-animation]');

    scrollElements.forEach(element => {
      const rect = element.getBoundingClientRect();
      const isVisible = rect.top < this.viewport.height && rect.bottom > 0;

      if (isVisible && !element.classList.contains('animated')) {
        const animation = element.getAttribute('data-scroll-animation');
        element.style.animation = `${animation} 0.6s ease-out forwards`;
        element.classList.add('animated');
      }
    });
  }

  pauseAnimations() {
    // Pause particle systems
    if (window.heroParticleSystem) {
      window.heroParticleSystem.pause();
    }
    if (window.showcaseParticleSystem) {
      window.showcaseParticleSystem.pause();
    }
  }

  resumeAnimations() {
    // Resume particle systems
    if (window.heroParticleSystem) {
      window.heroParticleSystem.start();
    }
    if (window.showcaseParticleSystem) {
      window.showcaseParticleSystem.start();
    }
  }

  focusSearch() {
    const searchInput = document.querySelector('input[type="search"]');
    if (searchInput) {
      searchInput.focus();
    }
  }

  setupPerformanceMonitoring() {
    if (!this.performance.adaptiveQuality) return;

    setInterval(() => {
      const { fps } = this.performance;

      if (fps < 30) {
        this.reducePerformance();
      } else if (fps > 50 && this.performanceMode === 'low') {
        this.increasePerformance();
      }
    }, 3000);
  }

  monitorFrameRate() {
    const measureFPS = () => {
      const now = performance.now();
      const delta = now - this.performance.lastFrameTime;
      this.performance.fps = Math.round(1000 / delta);
      this.performance.lastFrameTime = now;

      requestAnimationFrame(measureFPS);
    };

    requestAnimationFrame(measureFPS);
  }

  reducePerformance() {
    if (this.performanceMode === 'low') return;

    this.performanceMode = 'low';
    console.log('Performance reduced to low mode');

    // Reduce particle counts
    if (window.heroParticleSystem) {
      window.heroParticleSystem.updateOptions({ particleCount: 20 });
    }
  }

  increasePerformance() {
    if (this.performanceMode === 'high') return;

    this.performanceMode = 'high';
    console.log('Performance increased to high mode');

    // Increase particle counts
    if (window.heroParticleSystem) {
      window.heroParticleSystem.updateOptions({ particleCount: 60 });
    }
  }

  setupAnalytics() {
    // Basic analytics setup
    this.analytics = {
      track: (event, data) => {
        // Simple analytics implementation
        console.log('Analytics:', event, data);

        // Send to analytics service if available
        if (window.gtag) {
          gtag('event', event, data);
        }
      }
    };

    // Track page view
    this.analytics.track('page_view', {
      page_path: window.location.pathname
    });

    // Track performance mode
    this.analytics.track('performance_mode', {
      mode: this.performanceMode
    });
  }

  announceFilterChange(category) {
    const announcement = `Showing ${category === 'all' ? 'all features' : category + ' features'}`;

    // Create or update live region
    let liveRegion = document.getElementById('filter-live-region');
    if (!liveRegion) {
      liveRegion = document.createElement('div');
      liveRegion.id = 'filter-live-region';
      liveRegion.setAttribute('aria-live', 'polite');
      liveRegion.setAttribute('aria-atomic', 'true');
      liveRegion.className = 'sr-only';
      document.body.appendChild(liveRegion);
    }

    liveRegion.textContent = announcement;
  }

  triggerEvent(eventName, data = {}) {
    const event = new CustomEvent(eventName, { detail: data });
    document.dispatchEvent(event);
  }

  // Utility functions
  throttle(func, limit) {
    let inThrottle;
    return function() {
      const args = arguments;
      const context = this;
      if (!inThrottle) {
        func.apply(context, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  }

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

  // Public API
  getPerformanceMetrics() {
    return {
      fps: this.performance.fps,
      mode: this.performanceMode,
      reducedMotion: this.reducedMotion,
      capabilities: this.capabilities
    };
  }

  destroy() {
    // Clean up event listeners and resources
    this.pauseAnimations();

    if (this.scrollObserver) {
      this.scrollObserver.disconnect();
    }

    // Remove event listeners
    window.removeEventListener('scroll', this.throttledUpdateActiveStates);
    window.removeEventListener('scroll', this.throttledParallax);
  }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
  window.signatureExtractorLanding = new SignatureExtractorLanding();

  // Make app globally available for debugging
  window.app = window.signatureExtractorLanding;
});

// Export for module systems
// Make available globally for non-module usage
window.SignatureExtractorLanding = SignatureExtractorLanding;