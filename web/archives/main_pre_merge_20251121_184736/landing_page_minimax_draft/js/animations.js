/* ============================================
   Advanced Animations
   Beautiful, smooth, performance-optimized animations
   ============================================ */

// Animation Manager
class AnimationManager {
  constructor() {
    this.animations = new Map();
    this.observers = new Map();
    this.performanceMode = this.detectPerformanceMode();
    this.init();
  }

  init() {
    this.initScrollAnimations();
    this.initHoverAnimations();
    this.initTypewriterAnimations();
    this.initParticleEffects();
    this.initMorphingEffects();
    this.initRevealAnimations();
  }

  detectPerformanceMode() {
    // Detect if device can handle complex animations
    return navigator.hardwareConcurrency && navigator.hardwareConcurrency >= 4;
  }

  // Scroll-triggered animations
  initScrollAnimations() {
    const animatedElements = document.querySelectorAll(
      '.animate-on-scroll, [data-animate]'
    );

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const element = entry.target;
          const animationType = element.dataset.animate || 'fade-up';
          const delay = element.dataset.delay || 0;

          if (entry.isIntersecting && !element.classList.contains('animated')) {
            setTimeout(() => {
              this.triggerAnimation(element, animationType);
              element.classList.add('animated');
            }, delay);

            // Unobserve after animation
            observer.unobserve(element);
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px',
      }
    );

    animatedElements.forEach((element) => observer.observe(element));
    this.observers.set('scroll', observer);
  }

  // Hover animations
  initHoverAnimations() {
    // Magnetic effect for buttons
    const magneticElements = document.querySelectorAll(
      '.btn, .feature-card, .use-case-card'
    );

    magneticElements.forEach((element) => {
      element.addEventListener('mousemove', (e) => {
        this.magneticEffect(e, element);
      });

      element.addEventListener('mouseleave', (e) => {
        this.resetMagneticEffect(e, element);
      });
    });

    // Glow effects
    const glowElements = document.querySelectorAll(
      '.pricing-card, .hero-cta .btn'
    );
    glowElements.forEach((element) => {
      element.addEventListener('mouseenter', () => {
        element.classList.add('animate-glow');
      });

      element.addEventListener('mouseleave', () => {
        element.classList.remove('animate-glow');
      });
    });

    // Tilt effect
    const tiltElements = document.querySelectorAll(
      '.feature-card, .use-case-card, .testimonial-card'
    );
    tiltElements.forEach((element) => {
      element.addEventListener('mousemove', (e) => {
        this.tiltEffect(e, element);
      });

      element.addEventListener('mouseleave', () => {
        this.resetTiltEffect(element);
      });
    });
  }

  // Typewriter animations
  initTypewriterAnimations() {
    const typewriterElements = document.querySelectorAll(
      '.typewriter, [data-typewriter]'
    );

    typewriterElements.forEach((element) => {
      const text = element.dataset.typewriter || element.textContent;
      const speed = parseInt(element.dataset.speed) || 50;

      if (text && text.length > 0) {
        this.typewriterEffect(element, text, speed);
      }
    });
  }

  // Particle effects
  initParticleEffects() {
    if (!this.performanceMode) return;

    const particleContainers = document.querySelectorAll('[data-particles]');

    particleContainers.forEach((container) => {
      this.createParticleEffect(container);
    });
  }

  // Morphing effects
  initMorphingEffects() {
    const morphElements = document.querySelectorAll('[data-morph]');

    morphElements.forEach((element) => {
      element.addEventListener('mouseenter', () => {
        element.classList.add('morph');
      });

      element.addEventListener('mouseleave', () => {
        element.classList.remove('morph');
      });
    });
  }

  // Reveal animations
  initRevealAnimations() {
    const revealElements = document.querySelectorAll('[data-reveal]');

    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const element = entry.target;
            const direction = element.dataset.reveal || 'up';
            const delay = element.dataset.delay || 0;

            setTimeout(() => {
              this.revealEffect(element, direction);
            }, delay);

            revealObserver.unobserve(element);
          }
        });
      },
      {
        threshold: 0.1,
      }
    );

    revealElements.forEach((element) => revealObserver.observe(element));
  }

  // Magnetic effect implementation
  magneticEffect(event, element) {
    const rect = element.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    const deltaX = (event.clientX - centerX) * 0.1;
    const deltaY = (event.clientY - centerY) * 0.1;

    element.style.transform = `translate(${deltaX}px, ${deltaY}px) scale(1.05)`;
  }

  resetMagneticEffect(event, element) {
    element.style.transform = '';
  }

  // Tilt effect implementation
  tiltEffect(event, element) {
    const rect = element.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    const rotateX = (event.clientY - centerY) / 10;
    const rotateY = (centerX - event.clientX) / 10;

    element.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
    element.style.transition = 'none';
  }

  resetTiltEffect(element) {
    element.style.transform = '';
    element.style.transition = 'transform 0.3s ease';
  }

  // Typewriter effect implementation
  typewriterEffect(element, text, speed) {
    element.textContent = '';
    element.style.borderRight = '2px solid #007AFF';

    let i = 0;
    const timer = setInterval(() => {
      element.textContent += text.charAt(i);
      i++;

      if (i >= text.length) {
        clearInterval(timer);
        setTimeout(() => {
          element.style.borderRight = 'none';
        }, 1000);
      }
    }, speed);
  }

  // Particle effect implementation
  createParticleEffect(container) {
    const particleCount = 20;
    const particles = [];

    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.cssText = `
                position: absolute;
                width: 2px;
                height: 2px;
                background: rgba(0, 122, 255, 0.3);
                border-radius: 50%;
                pointer-events: none;
                animation: float ${3 + Math.random() * 4}s ease-in-out infinite;
                animation-delay: ${Math.random() * 2}s;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
            `;

      container.appendChild(particle);
      particles.push(particle);
    }
  }

  // Reveal effect implementation
  revealEffect(element, direction) {
    const animations = {
      up: { transform: 'translateY(0)', opacity: 1 },
      down: { transform: 'translateY(0)', opacity: 1 },
      left: { transform: 'translateX(0)', opacity: 1 },
      right: { transform: 'translateX(0)', opacity: 1 },
      scale: { transform: 'scale(1)', opacity: 1 },
      rotate: { transform: 'rotate(0deg)', opacity: 1 },
    };

    const animation = animations[direction] || animations.up;

    element.style.opacity = 0;

    if (direction === 'up') element.style.transform = 'translateY(50px)';
    if (direction === 'down') element.style.transform = 'translateY(-50px)';
    if (direction === 'left') element.style.transform = 'translateX(50px)';
    if (direction === 'right') element.style.transform = 'translateX(-50px)';
    if (direction === 'scale') element.style.transform = 'scale(0.8)';
    if (direction === 'rotate')
      element.style.transform = 'rotate(10deg) scale(0.8)';

    setTimeout(() => {
      element.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
      Object.assign(element.style, animation);
    }, 50);
  }

  // Trigger specific animation
  triggerAnimation(element, type) {
    const animations = {
      'fade-up': () => {
        element.style.opacity = 0;
        element.style.transform = 'translateY(30px)';
        setTimeout(() => {
          element.style.transition = 'all 0.6s ease-out';
          element.style.opacity = 1;
          element.style.transform = 'translateY(0)';
        }, 50);
      },
      'fade-left': () => {
        element.style.opacity = 0;
        element.style.transform = 'translateX(-30px)';
        setTimeout(() => {
          element.style.transition = 'all 0.6s ease-out';
          element.style.opacity = 1;
          element.style.transform = 'translateX(0)';
        }, 50);
      },
      'fade-right': () => {
        element.style.opacity = 0;
        element.style.transform = 'translateX(30px)';
        setTimeout(() => {
          element.style.transition = 'all 0.6s ease-out';
          element.style.opacity = 1;
          element.style.transform = 'translateX(0)';
        }, 50);
      },
      scale: () => {
        element.style.opacity = 0;
        element.style.transform = 'scale(0.8)';
        setTimeout(() => {
          element.style.transition = 'all 0.6s ease-out';
          element.style.opacity = 1;
          element.style.transform = 'scale(1)';
        }, 50);
      },
      rotate: () => {
        element.style.opacity = 0;
        element.style.transform = 'rotate(-10deg) scale(0.8)';
        setTimeout(() => {
          element.style.transition = 'all 0.6s ease-out';
          element.style.opacity = 1;
          element.style.transform = 'rotate(0deg) scale(1)';
        }, 50);
      },
    };

    const animation = animations[type] || animations['fade-up'];
    animation();
  }

  // Clean up
  destroy() {
    this.observers.forEach((observer) => observer.disconnect());
    this.observers.clear();
    this.animations.clear();
  }
}

// Parallax effect class
class ParallaxEffect {
  constructor() {
    this.elements = [];
    this.enabled = this.detectSupport();
    this.init();
  }

  detectSupport() {
    return 'IntersectionObserver' in window && !this.isMobile();
  }

  isMobile() {
    return (
      window.innerWidth <= 768 ||
      /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
        navigator.userAgent
      )
    );
  }

  init() {
    if (!this.enabled) return;

    const parallaxElements = document.querySelectorAll('[data-parallax]');

    parallaxElements.forEach((element) => {
      this.elements.push({
        element,
        speed: parseFloat(element.dataset.parallax) || 0.5,
      });
    });

    this.bindEvents();
  }

  bindEvents() {
    let ticking = false;

    const updateParallax = () => {
      const scrollY = window.pageYOffset;

      this.elements.forEach(({ element, speed }) => {
        const yPos = -(scrollY * speed);
        element.style.transform = `translate3d(0, ${yPos}px, 0)`;
      });

      ticking = false;
    };

    const requestTick = () => {
      if (!ticking) {
        requestAnimationFrame(updateParallax);
        ticking = true;
      }
    };

    window.addEventListener('scroll', requestTick, { passive: true });
  }

  destroy() {
    this.elements = [];
  }
}

// Smooth reveal on scroll
class RevealOnScroll {
  constructor() {
    this.elements = [];
    this.init();
  }

  init() {
    const revealElements = document.querySelectorAll('[data-reveal]');

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const element = entry.target;
            const animation = element.dataset.reveal || 'fade';
            const duration = parseInt(element.dataset.duration) || 600;
            const delay = parseInt(element.dataset.delay) || 0;

            setTimeout(() => {
              this.animateElement(element, animation, duration);
            }, delay);

            observer.unobserve(element);
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px',
      }
    );

    revealElements.forEach((element) => observer.observe(element));
  }

  animateElement(element, animation, duration) {
    element.style.transition = `all ${duration}ms cubic-bezier(0.4, 0, 0.2, 1)`;

    switch (animation) {
      case 'fade':
        element.style.opacity = 1;
        break;
      case 'slide-up':
        element.style.opacity = 1;
        element.style.transform = 'translateY(0)';
        break;
      case 'slide-down':
        element.style.opacity = 1;
        element.style.transform = 'translateY(0)';
        break;
      case 'slide-left':
        element.style.opacity = 1;
        element.style.transform = 'translateX(0)';
        break;
      case 'slide-right':
        element.style.opacity = 1;
        element.style.transform = 'translateX(0)';
        break;
      case 'zoom':
        element.style.opacity = 1;
        element.style.transform = 'scale(1)';
        break;
      case 'flip':
        element.style.opacity = 1;
        element.style.transform = 'rotateY(0deg)';
        break;
    }
  }
}

// Initialize animations when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.animationManager = new AnimationManager();
  window.parallaxEffect = new ParallaxEffect();
  window.revealOnScroll = new RevealOnScroll();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
  if (window.animationManager) {
    window.animationManager.destroy();
  }
  if (window.parallaxEffect) {
    window.parallaxEffect.destroy();
  }
});

// Export for use in other scripts
window.AnimationUtils = {
  AnimationManager,
  ParallaxEffect,
  RevealOnScroll,
};
