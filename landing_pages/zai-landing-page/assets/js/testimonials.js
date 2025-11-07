/**
 * Testimonials Carousel Controller
 * Handles the testimonials section with smooth transitions
 */

class TestimonialsCarousel {
  constructor() {
    this.currentIndex = 0;
    this.testimonials = [];
    this.isPlaying = true;
    this.autoplayInterval = null;
    this.autoplayDelay = 6000; // 6 seconds
    this.isTransitioning = false;

    this.init();
  }

  init() {
    this.setupTestimonials();
    this.setupEventListeners();
    this.setupKeyboardNavigation();
    this.startAutoplay();
    this.setupAccessibility();
  }

  /**
   * Setup testimonials array
   */
  setupTestimonials() {
    const testimonialCards = document.querySelectorAll('.testimonial-card');
    this.testimonials = Array.from(testimonialCards);

    if (this.testimonials.length === 0) {
      console.warn('No testimonial cards found');
      return;
    }

    // Initialize first testimonial
    this.updateTestimonial();
  }

  /**
   * Setup event listeners
   */
  setupEventListeners() {
    // Previous button
    const prevBtn = document.getElementById('testimonial-prev');
    if (prevBtn) {
      prevBtn.addEventListener('click', () => this.previous());
    }

    // Next button
    const nextBtn = document.getElementById('testimonial-next');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => this.next());
    }

    // Indicator buttons
    const indicators = document.querySelectorAll('.indicator');
    indicators.forEach((indicator, index) => {
      indicator.addEventListener('click', () => this.goToTestimonial(index));
    });

    // Pause on hover
    const testimonialsSection = document.querySelector('.testimonials');
    if (testimonialsSection) {
      testimonialsSection.addEventListener('mouseenter', () => {
        if (this.isPlaying) {
          this.stopAutoplay();
        }
      });

      testimonialsSection.addEventListener('mouseleave', () => {
        if (this.isPlaying) {
          this.startAutoplay();
        }
      });
    }

    // Handle visibility changes
    document.addEventListener('visibilitychange', () => {
      if (document.hidden && this.isPlaying) {
        this.stopAutoplay();
      } else if (!document.hidden && this.isPlaying) {
        this.startAutoplay();
      }
    });

    // Touch support for mobile
    this.setupTouchSupport();
  }

  /**
   * Setup keyboard navigation
   */
  setupKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
      const testimonialsSection = document.querySelector('.testimonials');
      if (!testimonialsSection) return;

      // Only handle keyboard events when testimonials section is in view
      const rect = testimonialsSection.getBoundingClientRect();
      const isInView = rect.top < window.innerHeight && rect.bottom > 0;

      if (!isInView) return;

      switch (e.key) {
        case 'ArrowLeft':
          e.preventDefault();
          this.previous();
          break;
        case 'ArrowRight':
          e.preventDefault();
          this.next();
          break;
        case 'Home':
          e.preventDefault();
          this.goToTestimonial(0);
          break;
        case 'End':
          e.preventDefault();
          this.goToTestimonial(this.testimonials.length - 1);
          break;
        case ' ':
          e.preventDefault();
          this.toggleAutoplay();
          break;
      }
    });
  }

  /**
   * Setup accessibility features
   */
  setupAccessibility() {
    const carousel = document.querySelector('.testimonials-carousel');
    if (!carousel) return;

    // Add ARIA attributes
    carousel.setAttribute('role', 'region');
    carousel.setAttribute('aria-label', 'Customer testimonials');
    carousel.setAttribute('aria-roledescription', 'carousel');

    // Update testimonial attributes
    this.testimonials.forEach((testimonial, index) => {
      testimonial.setAttribute('role', 'group');
      testimonial.setAttribute('aria-roledescription', 'slide');
      testimonial.setAttribute('aria-label', `Testimonial ${index + 1} of ${this.testimonials.length}`);
      testimonial.setAttribute('aria-hidden', index !== this.currentIndex ? 'true' : 'false');
    });

    // Update controls
    this.updateControlsAccessibility();
  }

  /**
   * Setup touch support for mobile swiping
   */
  setupTouchSupport() {
    const carousel = document.querySelector('.testimonials-carousel');
    if (!carousel) return;

    let touchStartX = 0;
    let touchEndX = 0;
    let touchStartY = 0;
    let touchEndY = 0;

    const handleTouchStart = (e) => {
      touchStartX = e.changedTouches[0].screenX;
      touchStartY = e.changedTouches[0].screenY;
    };

    const handleTouchEnd = (e) => {
      touchEndX = e.changedTouches[0].screenX;
      touchEndY = e.changedTouches[0].screenY;
      this.handleSwipe();
    };

    carousel.addEventListener('touchstart', handleTouchStart, { passive: true });
    carousel.addEventListener('touchend', handleTouchEnd, { passive: true });

    this.handleSwipe = () => {
      const deltaX = touchEndX - touchStartX;
      const deltaY = touchEndY - touchStartY;
      const minSwipeDistance = 50;

      // Only handle horizontal swipes
      if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > minSwipeDistance) {
        if (deltaX > 0) {
          this.previous();
        } else {
          this.next();
        }
      }
    };
  }

  /**
   * Go to previous testimonial
   */
  previous() {
    if (this.isTransitioning) return;

    this.currentIndex = (this.currentIndex - 1 + this.testimonials.length) % this.testimonials.length;
    this.updateTestimonial();
    this.resetAutoplay();
  }

  /**
   * Go to next testimonial
   */
  next() {
    if (this.isTransitioning) return;

    this.currentIndex = (this.currentIndex + 1) % this.testimonials.length;
    this.updateTestimonial();
    this.resetAutoplay();
  }

  /**
   * Go to specific testimonial
   */
  goToTestimonial(index) {
    if (this.isTransitioning || index === this.currentIndex) return;

    if (index >= 0 && index < this.testimonials.length) {
      this.currentIndex = index;
      this.updateTestimonial();
      this.resetAutoplay();
    }
  }

  /**
   * Update testimonial display
   */
  updateTestimonial() {
    if (this.isTransitioning) return;

    this.isTransitioning = true;

    // Update testimonial cards
    this.testimonials.forEach((testimonial, index) => {
      const isActive = index === this.currentIndex;

      // Update classes
      testimonial.classList.toggle('active', isActive);

      // Update accessibility
      testimonial.setAttribute('aria-hidden', !isActive ? 'true' : 'false');

      // Focus management
      if (isActive) {
        testimonial.removeAttribute('tabindex');
        testimonial.removeAttribute('aria-hidden');
      } else {
        testimonial.setAttribute('tabindex', '-1');
      }
    });

    // Update indicators
    this.updateIndicators();

    // Update controls
    this.updateControls();

    // Update accessibility
    this.updateControlsAccessibility();

    // Announce to screen readers
    this.announceTestimonialChange();

    // Track analytics
    this.trackTestimonialView();

    // Reset transition flag after animation
    setTimeout(() => {
      this.isTransitioning = false;
    }, 600);
  }

  /**
   * Update indicator buttons
   */
  updateIndicators() {
    const indicators = document.querySelectorAll('.indicator');
    indicators.forEach((indicator, index) => {
      indicator.classList.toggle('active', index === this.currentIndex);
      indicator.setAttribute('aria-selected', index === this.currentIndex ? 'true' : 'false');
      indicator.setAttribute('aria-label', `Go to testimonial ${index + 1}`);
    });
  }

  /**
   * Update control buttons
   */
  updateControls() {
    const prevBtn = document.getElementById('testimonial-prev');
    const nextBtn = document.getElementById('testimonial-next');

    if (prevBtn) {
      prevBtn.disabled = this.isTransitioning;
      prevBtn.setAttribute('aria-label', `Previous testimonial (${this.currentIndex} of ${this.testimonials.length})`);
    }

    if (nextBtn) {
      nextBtn.disabled = this.isTransitioning;
      nextBtn.setAttribute('aria-label', `Next testimonial (${this.currentIndex + 2} of ${this.testimonials.length})`);
    }
  }

  /**
   * Update controls accessibility
   */
  updateControlsAccessibility() {
    const carousel = document.querySelector('.testimonials-carousel');
    if (!carousel) return;

    carousel.setAttribute('aria-label', `Customer testimonials, showing testimonial ${this.currentIndex + 1} of ${this.testimonials.length}`);
  }

  /**
   * Announce testimonial change to screen readers
   */
  announceTestimonialChange() {
    const testimonial = this.testimonials[this.currentIndex];
    const authorName = testimonial.querySelector('.author-name')?.textContent || 'Unknown';
    const announcement = `Now showing testimonial ${this.currentIndex + 1} of ${this.testimonials.length} from ${authorName}`;

    // Create or update live region
    let liveRegion = document.getElementById('testimonial-live-region');
    if (!liveRegion) {
      liveRegion = document.createElement('div');
      liveRegion.id = 'testimonial-live-region';
      liveRegion.setAttribute('aria-live', 'polite');
      liveRegion.setAttribute('aria-atomic', 'true');
      liveRegion.className = 'sr-only';
      document.body.appendChild(liveRegion);
    }

    liveRegion.textContent = announcement;
  }

  /**
   * Start autoplay
   */
  startAutoplay() {
    this.stopAutoplay();
    this.isPlaying = true;

    this.autoplayInterval = setInterval(() => {
      this.next();
    }, this.autoplayDelay);
  }

  /**
   * Stop autoplay
   */
  stopAutoplay() {
    if (this.autoplayInterval) {
      clearInterval(this.autoplayInterval);
      this.autoplayInterval = null;
    }
    this.isPlaying = false;
  }

  /**
   * Toggle autoplay
   */
  toggleAutoplay() {
    if (this.isPlaying) {
      this.stopAutoplay();
    } else {
      this.startAutoplay();
    }
  }

  /**
   * Reset autoplay timer
   */
  resetAutoplay() {
    if (this.isPlaying) {
      this.stopAutoplay();
      this.startAutoplay();
    }
  }

  /**
   * Track testimonial view for analytics
   */
  trackTestimonialView() {
    const testimonial = this.testimonials[this.currentIndex];
    const authorName = testimonial.querySelector('.author-name')?.textContent || 'Unknown';

    if (typeof window.signatureExtractorLanding !== 'undefined') {
      window.signatureExtractorLanding.trackEvent('testimonial_view', {
        testimonialIndex: this.currentIndex + 1,
        authorName: authorName,
        autoplay: this.isPlaying
      });
    }
  }

  /**
   * Get current state
   */
  getState() {
    return {
      currentIndex: this.currentIndex,
      totalTestimonials: this.testimonials.length,
      isPlaying: this.isPlaying,
      isTransitioning: this.isTransitioning,
      autoplayDelay: this.autoplayDelay
    };
  }

  /**
   * Update configuration
   */
  updateConfig(newConfig) {
    if (newConfig.autoplayDelay !== undefined) {
      this.autoplayDelay = newConfig.autoplayDelay;
      if (this.isPlaying) {
        this.resetAutoplay();
      }
    }

    if (newConfig.autoPlay !== undefined) {
      if (newConfig.autoPlay && !this.isPlaying) {
        this.startAutoplay();
      } else if (!newConfig.autoPlay && this.isPlaying) {
        this.stopAutoplay();
      }
    }
  }

  /**
   * Destroy the carousel
   */
  destroy() {
    this.stopAutoplay();

    // Remove event listeners
    document.removeEventListener('keydown', this.setupKeyboardNavigation);

    // Clean up live region
    const liveRegion = document.getElementById('testimonial-live-region');
    if (liveRegion) {
      liveRegion.remove();
    }

    // Remove touch event listeners
    const carousel = document.querySelector('.testimonials-carousel');
    if (carousel) {
      carousel.removeEventListener('touchstart', this.handleTouchStart);
      carousel.removeEventListener('touchend', this.handleTouchEnd);
    }

    this.testimonials = [];
  }
}

// Initialize testimonials carousel when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  // Wait a bit for other scripts to load
  setTimeout(() => {
    if (document.querySelector('.testimonials-carousel')) {
      window.testimonialsCarousel = new TestimonialsCarousel();
    }
  }, 100);
});

// Handle resize events
let resizeTimeout;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    // Trigger any resize-dependent logic
    window.dispatchEvent(new CustomEvent('testimonials-resize'));
  }, 250);
});

// Clean up on page unload
window.addEventListener('beforeunload', () => {
  if (window.testimonialsCarousel) {
    window.testimonialsCarousel.destroy();
  }
});

// Export for potential use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = TestimonialsCarousel;
}