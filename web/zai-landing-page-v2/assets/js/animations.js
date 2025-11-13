/**
 * Signature Extractor - Animation Controller
 * Centralized animation management for the landing page
 */

class AnimationController {
  constructor() {
    this.animations = [];
    this.observers = [];
    this.isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    this.isLowPerformance = false;
    this.ticking = false;

    this.init();
  }

  init() {
    this.setupIntersectionObserver();
    this.setupScrollAnimations();
    this.setupLoadingAnimations();
    this.setupPerformanceMonitoring();
  }

  setupIntersectionObserver() {
    if (!('IntersectionObserver' in window) || this.isReducedMotion) {
      this.fallbackAnimations();
      return;
    }

    this.intersectionObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.animateElement(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });

    // Observe all elements with animation data attributes
    this.observeAnimatedElements();
  }

  observeAnimatedElements() {
    const elements = document.querySelectorAll('[data-animate], [data-scroll-animation]');
    elements.forEach(element => {
      this.intersectionObserver.observe(element);
    });
  }

  fallbackAnimations() {
    // Fallback for browsers without Intersection Observer
    const elements = document.querySelectorAll('[data-animate], [data-scroll-animation]');
    elements.forEach(element => {
      // Show elements immediately
      element.classList.add('animate-in');
    });
  }

  setupScrollAnimations() {
    let lastScrollY = window.pageYOffset;
    const scrollElements = document.querySelectorAll('[data-parallax], [data-scroll-scale]');

    const updateScrollAnimations = () => {
      const scrollY = window.pageYOffset;
      const deltaY = scrollY - lastScrollY;
      const direction = deltaY > 0 ? 'down' : 'up';

      scrollElements.forEach(element => {
        this.updateScrollElement(element, scrollY, direction);
      });

      lastScrollY = scrollY;
      this.ticking = false;
    };

    const requestTick = () => {
      if (!this.ticking) {
        requestAnimationFrame(updateScrollAnimations);
        this.ticking = true;
      }
    };

    window.addEventListener('scroll', requestTick);
  }

  updateScrollElement(element, scrollY, direction) {
    const rect = element.getBoundingClientRect();
    const speed = parseFloat(element.dataset.parallax) || 0.5;
    const scale = parseFloat(element.dataset.scrollScale) || 1;

    if (element.dataset.parallax) {
      const yPos = -(scrollY * speed);
      element.style.transform = `translateY(${yPos}px)`;
    }

    if (element.dataset.scrollScale) {
      const viewportCenter = window.innerHeight / 2;
      const elementCenter = rect.top + rect.height / 2;
      const distance = Math.abs(viewportCenter - elementCenter);
      const maxDistance = viewportCenter;
      const scaleAmount = Math.max(0, 1 - (distance / maxDistance) * (1 - scale));

      element.style.transform = `scale(${scaleAmount})`;
    }
  }

  setupLoadingAnimations() {
    // Animate loading signature
    const loadingPath = document.querySelector('.loading-path');
    if (loadingPath) {
      const length = loadingPath.getTotalLength();
      loadingPath.style.strokeDasharray = length;
      loadingPath.style.strokeDashoffset = length;

      // Trigger animation after a small delay
      setTimeout(() => {
        loadingPath.style.transition = 'stroke-dashoffset 2s ease-in-out';
        loadingPath.style.strokeDashoffset = 0;
      }, 100);
    }

    // Animate loading bar
    const loadingBar = document.querySelector('.loading-bar');
    if (loadingBar) {
      setTimeout(() => {
        loadingBar.style.width = '100%';
      }, 200);
    }
  }

  setupPerformanceMonitoring() {
    // Simple performance check
    let frames = 0;
    let lastTime = performance.now();

    const checkPerformance = (currentTime) => {
      frames++;

      if (currentTime >= lastTime + 1000) {
        const fps = Math.round((frames * 1000) / (currentTime - lastTime));

        if (fps < 30) {
          this.isLowPerformance = true;
          this.reduceAnimations();
        }

        frames = 0;
        lastTime = currentTime;
      }

      if (!this.isLowPerformance) {
        requestAnimationFrame(checkPerformance);
      }
    };

    requestAnimationFrame(checkPerformance);
  }

  reduceAnimations() {
    // Disable or reduce complex animations for low-performance devices
    document.body.classList.add('reduce-animations');

    // Reduce particle counts if particle systems exist
    if (window.heroParticleSystem) {
      window.heroParticleSystem.updateOptions({
        particleCount: 20,
        connectionDistance: 80
      });
    }
  }

  animateElement(element) {
    const animationType = element.dataset.animate || element.dataset.scrollAnimation;

    // Remove from observer
    this.intersectionObserver.unobserve(element);

    // Add animation class
    element.classList.add('animate-in');

    // Apply specific animation based on type
    switch (animationType) {
      case 'fade-in-up':
        this.animateFadeInUp(element);
        break;
      case 'fade-in-left':
        this.animateFadeInLeft(element);
        break;
      case 'fade-in-right':
        this.animateFadeInRight(element);
        break;
      case 'scale-in':
        this.animateScaleIn(element);
        break;
      case 'slide-in-up':
        this.animateSlideInUp(element);
        break;
      case 'slide-in-down':
        this.animateSlideInDown(element);
        break;
      default:
        this.animateDefault(element);
    }
  }

  animateFadeInUp(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateY(30px)';
    element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';

    requestAnimationFrame(() => {
      element.style.opacity = '1';
      element.style.transform = 'translateY(0)';
    });
  }

  animateFadeInLeft(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateX(-30px)';
    element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';

    requestAnimationFrame(() => {
      element.style.opacity = '1';
      element.style.transform = 'translateX(0)';
    });
  }

  animateFadeInRight(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateX(30px)';
    element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';

    requestAnimationFrame(() => {
      element.style.opacity = '1';
      element.style.transform = 'translateX(0)';
    });
  }

  animateScaleIn(element) {
    element.style.opacity = '0';
    element.style.transform = 'scale(0.8)';
    element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';

    requestAnimationFrame(() => {
      element.style.opacity = '1';
      element.style.transform = 'scale(1)';
    });
  }

  animateSlideInUp(element) {
    element.style.transform = 'translateY(100%)';
    element.style.transition = 'transform 0.8s cubic-bezier(0.4, 0, 0.2, 1)';

    requestAnimationFrame(() => {
      element.style.transform = 'translateY(0)';
    });
  }

  animateSlideInDown(element) {
    element.style.transform = 'translateY(-100%)';
    element.style.transition = 'transform 0.8s cubic-bezier(0.4, 0, 0.2, 1)';

    requestAnimationFrame(() => {
      element.style.transform = 'translateY(0)';
    });
  }

  animateDefault(element) {
    element.style.opacity = '0';
    element.style.transition = 'opacity 0.6s ease-out';

    requestAnimationFrame(() => {
      element.style.opacity = '1';
    });
  }

  // Staggered animations for lists
  animateList(elements, delay = 100) {
    elements.forEach((element, index) => {
      setTimeout(() => {
        this.animateElement(element);
      }, index * delay);
    });
  }

  // Counter animation
  animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;

    const updateCounter = () => {
      current += increment;
      if (current < target) {
        element.textContent = Math.floor(current);
        requestAnimationFrame(updateCounter);
      } else {
        element.textContent = target;
      }
    };

    updateCounter();
  }

  // Typewriter effect
  typewriter(element, text, speed = 50) {
    let index = 0;
    element.textContent = '';

    const type = () => {
      if (index < text.length) {
        element.textContent += text.charAt(index);
        index++;
        setTimeout(type, speed);
      }
    };

    type();
  }

  // Morphing animation
  morphSVG(element, toPath, duration = 1000) {
    const fromPath = element.getAttribute('d');
    const steps = 60;
    const stepDuration = duration / steps;
    let currentStep = 0;

    const animate = () => {
      currentStep++;
      const progress = currentStep / steps;
      const newPath = this.interpolatePath(fromPath, toPath, progress);
      element.setAttribute('d', newPath);

      if (currentStep < steps) {
        setTimeout(animate, stepDuration);
      }
    };

    animate();
  }

  interpolatePath(fromPath, toPath, progress) {
    // Simple path interpolation (could be enhanced)
    return progress < 0.5 ? fromPath : toPath;
  }

  // Public methods
  destroy() {
    if (this.intersectionObserver) {
      this.intersectionObserver.disconnect();
    }

    // Clean up event listeners
    window.removeEventListener('scroll', this.requestTick);
  }
}

// Initialize animations
document.addEventListener('DOMContentLoaded', () => {
  window.animationController = new AnimationController();

  // Auto-animate elements with specific classes
  const animateElements = document.querySelectorAll('.animate-on-load');
  if (animateElements.length) {
    setTimeout(() => {
      animateElements.forEach((element, index) => {
        setTimeout(() => {
          window.animationController.animateElement(element);
        }, index * 200);
      });
    }, 500);
  }

  // Animate stats/numbers
  const statNumbers = document.querySelectorAll('[data-counter]');
  statNumbers.forEach(element => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const target = parseInt(element.dataset.counter);
          window.animationController.animateCounter(element, target);
          observer.unobserve(element);
        }
      });
    });

    observer.observe(element);
  });

  // Animate feature cards
  const featureCards = document.querySelectorAll('.feature-card');
  if (featureCards.length) {
    const featureObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            window.animationController.animateElement(entry.target);
          }, index * 150);
          featureObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    featureCards.forEach(card => featureObserver.observe(card));
  }
});

// Make available globally for non-module usage
window.AnimationController = AnimationController;