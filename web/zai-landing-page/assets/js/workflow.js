/**
 * Workflow Animation Controller
 * Handles the animated workflow section with interactive steps
 */

class WorkflowAnimator {
  constructor() {
    this.currentStep = 0;
    this.totalSteps = 6;
    this.isPlaying = true;
    this.animationDuration = 8000; // 8 seconds total
    this.stepDuration = this.animationDuration / this.totalSteps;
    this.progressInterval = null;
    this.stepAnimations = {
      1: 'animate-step-upload',
      2: 'animate-step-analyze',
      3: 'animate-step-select',
      4: 'animate-step-extract',
      5: 'animate-step-extract',
      6: 'animate-step-upload'
    };

    this.init();
  }

  init() {
    this.setupEventListeners();
    this.startAnimation();
    this.updateProgressBar();
    this.setupKeyboardNavigation();
  }

  /**
   * Setup event listeners for workflow controls
   */
  setupEventListeners() {
    // Previous button
    const prevBtn = document.getElementById('workflow-prev');
    if (prevBtn) {
      prevBtn.addEventListener('click', () => this.previousStep());
    }

    // Next button
    const nextBtn = document.getElementById('workflow-next');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => this.nextStep());
    }

    // Play/Pause button
    const playBtn = document.getElementById('workflow-play');
    if (playBtn) {
      playBtn.addEventListener('click', () => this.togglePlayPause());
    }

    // Step click interactions
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
      step.addEventListener('click', () => this.goToStep(index));
      step.addEventListener('mouseenter', () => this.previewStep(index));
      step.addEventListener('mouseleave', () => this.clearPreview());
    });

    // Pause animation on hover
    const workflowSection = document.querySelector('.workflow');
    if (workflowSection) {
      workflowSection.addEventListener('mouseenter', () => {
        if (this.isPlaying) {
          this.pauseAnimation();
        }
      });

      workflowSection.addEventListener('mouseleave', () => {
        if (this.isPlaying) {
          this.resumeAnimation();
        }
      });
    }

    // Handle visibility changes
    document.addEventListener('visibilitychange', () => {
      if (document.hidden && this.isPlaying) {
        this.pauseAnimation();
      } else if (!document.hidden && this.isPlaying) {
        this.resumeAnimation();
      }
    });
  }

  /**
   * Setup keyboard navigation
   */
  setupKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
      const workflowSection = document.querySelector('.workflow');
      if (!workflowSection) return;

      // Only handle keyboard events when workflow is in view
      const rect = workflowSection.getBoundingClientRect();
      const isInView = rect.top < window.innerHeight && rect.bottom > 0;

      if (!isInView) return;

      switch (e.key) {
        case 'ArrowLeft':
          e.preventDefault();
          this.previousStep();
          break;
        case 'ArrowRight':
          e.preventDefault();
          this.nextStep();
          break;
        case ' ':
          e.preventDefault();
          this.togglePlayPause();
          break;
        case 'Home':
          e.preventDefault();
          this.goToStep(0);
          break;
        case 'End':
          e.preventDefault();
          this.goToStep(this.totalSteps - 1);
          break;
      }
    });
  }

  /**
   * Start the automatic animation
   */
  startAnimation() {
    if (this.progressInterval) {
      clearInterval(this.progressInterval);
    }

    this.progressInterval = setInterval(() => {
      if (this.isPlaying) {
        this.nextStep();
      }
    }, this.stepDuration);

    this.updatePlayPauseButton();
  }

  /**
   * Go to next step
   */
  nextStep() {
    this.currentStep = (this.currentStep + 1) % this.totalSteps;
    this.updateStep();
  }

  /**
   * Go to previous step
   */
  previousStep() {
    this.currentStep = (this.currentStep - 1 + this.totalSteps) % this.totalSteps;
    this.updateStep();
  }

  /**
   * Go to specific step
   */
  goToStep(stepIndex) {
    if (stepIndex >= 0 && stepIndex < this.totalSteps) {
      this.currentStep = stepIndex;
      this.updateStep();
      this.resetProgressTimer();
    }
  }

  /**
   * Update the current step
   */
  updateStep() {
    // Update active step
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
      step.classList.toggle('step--active', index === this.currentStep);

      // Update step animation
      const animation = step.querySelector('.step-animation');
      if (animation) {
        // Remove all animation classes
        Object.values(this.stepAnimations).forEach(animClass => {
          animation.classList.remove(animClass);
        });

        // Add current step animation
        if (index === this.currentStep) {
          const animClass = this.stepAnimations[index + 1];
          if (animClass) {
            animation.classList.add(animClass);
          }
        }
      }

      // Update step indicator
      const indicator = step.querySelector('.step-indicator');
      if (indicator) {
        if (index === this.currentStep) {
          indicator.textContent = index + 1;
          indicator.style.background = 'var(--color-success)';
        } else if (index < this.currentStep) {
          indicator.textContent = '✓';
          indicator.style.background = 'var(--color-success)';
        } else {
          indicator.textContent = index + 1;
          indicator.style.background = 'var(--color-gray-300)';
        }
      }
    });

    // Update progress bar
    this.updateProgressBar();

    // Announce to screen readers
    this.announceStepChange();

    // Track analytics
    this.trackStepView(this.currentStep);
  }

  /**
   * Update progress bar
   */
  updateProgressBar() {
    const progressFill = document.querySelector('.progress-fill');
    if (progressFill) {
      const progress = ((this.currentStep + 1) / this.totalSteps) * 100;
      progressFill.style.width = `${progress}%`;
    }
  }

  /**
   * Reset progress timer
   */
  resetProgressTimer() {
    if (this.progressInterval) {
      clearInterval(this.progressInterval);
    }
    this.startAnimation();
  }

  /**
   * Toggle play/pause
   */
  togglePlayPause() {
    this.isPlaying = !this.isPlaying;
    this.updatePlayPauseButton();

    if (this.isPlaying) {
      this.resumeAnimation();
    } else {
      this.pauseAnimation();
    }

    this.trackEvent('workflow_play_pause', { playing: this.isPlaying });
  }

  /**
   * Pause animation
   */
  pauseAnimation() {
    this.isPlaying = false;
    this.updatePlayPauseButton();
  }

  /**
   * Resume animation
   */
  resumeAnimation() {
    this.isPlaying = true;
    this.updatePlayPauseButton();
  }

  /**
   * Update play/pause button
   */
  updatePlayPauseButton() {
    const playBtn = document.getElementById('workflow-play');
    if (!playBtn) return;

    const icon = playBtn.querySelector('svg');
    const text = playBtn.lastChild;

    if (this.isPlaying) {
      // Show pause icon
      icon.innerHTML = '<rect x="6" y="4" width="4" height="16" rx="1"/><rect x="10" y="4" width="4" height="16" rx="1"/>';
      text.textContent = 'Pause';
      playBtn.classList.add('playing');
    } else {
      // Show play icon
      icon.innerHTML = '<path d="M5 2L13 8L5 14V2Z"/>';
      text.textContent = 'Play';
      playBtn.classList.remove('playing');
    }
  }

  /**
   * Preview step on hover
   */
  previewStep(stepIndex) {
    if (stepIndex === this.currentStep) return;

    const step = document.querySelectorAll('.step')[stepIndex];
    if (step) {
      step.classList.add('step--preview');

      // Show step details
      this.showStepTooltip(step, stepIndex);
    }
  }

  /**
   * Clear step preview
   */
  clearPreview() {
    const steps = document.querySelectorAll('.step');
    steps.forEach(step => {
      step.classList.remove('step--preview');
    });

    this.hideStepTooltip();
  }

  /**
   * Show step tooltip
   */
  showStepTooltip(step, stepIndex) {
    const titles = [
      'Upload your document to get started',
      'AI analyzes and detects signatures automatically',
      'Select the signature area you want to extract',
      'Extract the signature with precision',
      'Preview the extracted signature',
      'Export in your preferred format'
    ];

    const tooltip = document.createElement('div');
    tooltip.className = 'step-tooltip';
    tooltip.textContent = titles[stepIndex];
    tooltip.setAttribute('role', 'tooltip');

    step.appendChild(tooltip);

    // Position tooltip
    setTimeout(() => {
      const rect = step.getBoundingClientRect();
      tooltip.style.bottom = `${rect.height + 10}px`;
      tooltip.style.left = '50%';
      tooltip.style.transform = 'translateX(-50%)';
    }, 10);
  }

  /**
   * Hide step tooltip
   */
  hideStepTooltip() {
    const tooltip = document.querySelector('.step-tooltip');
    if (tooltip) {
      tooltip.remove();
    }
  }

  /**
   * Announce step change to screen readers
   */
  announceStepChange() {
    const stepNames = [
      'Upload',
      'Analyze',
      'Select',
      'Extract',
      'Preview',
      'Export'
    ];

    const announcement = `Step ${this.currentStep + 1} of ${this.totalSteps}: ${stepNames[this.currentStep]}`;

    // Create or update live region
    let liveRegion = document.getElementById('workflow-live-region');
    if (!liveRegion) {
      liveRegion = document.createElement('div');
      liveRegion.id = 'workflow-live-region';
      liveRegion.setAttribute('aria-live', 'polite');
      liveRegion.setAttribute('aria-atomic', 'true');
      liveRegion.className = 'sr-only';
      document.body.appendChild(liveRegion);
    }

    liveRegion.textContent = announcement;
  }

  /**
   * Track step view for analytics
   */
  trackStepView(stepIndex) {
    const stepNames = ['upload', 'analyze', 'select', 'extract', 'preview', 'export'];

    if (typeof window.signatureExtractorLanding !== 'undefined') {
      window.signatureExtractorLanding.trackEvent('workflow_step_view', {
        step: stepIndex + 1,
        stepName: stepNames[stepIndex],
        autoplay: this.isPlaying
      });
    }
  }

  /**
   * Track general workflow events
   */
  trackEvent(eventName, data = {}) {
    if (typeof window.signatureExtractorLanding !== 'undefined') {
      window.signatureExtractorLanding.trackEvent(eventName, data);
    }
  }

  /**
   * Handle responsive layout changes
   */
  handleResize() {
    const workflow = document.querySelector('.workflow');
    if (!workflow) return;

    const isMobile = window.innerWidth < 768;
    workflow.classList.toggle('workflow--mobile', isMobile);

    // Adjust animation speed for mobile
    if (isMobile) {
      this.stepDuration = 10000; // Slower on mobile
    } else {
      this.stepDuration = 8000;
    }

    this.resetProgressTimer();
  }

  /**
   * Destroy the workflow animator
   */
  destroy() {
    if (this.progressInterval) {
      clearInterval(this.progressInterval);
    }

    // Remove event listeners
    document.removeEventListener('keydown', this.setupKeyboardNavigation);

    // Clean up live region
    const liveRegion = document.getElementById('workflow-live-region');
    if (liveRegion) {
      liveRegion.remove();
    }
  }
}

// Initialize workflow animator when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  // Wait a bit for other scripts to load
  setTimeout(() => {
    if (document.querySelector('.workflow')) {
      window.workflowAnimator = new WorkflowAnimator();
    }
  }, 100);
});

// Handle resize events
let resizeTimeout;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    if (window.workflowAnimator) {
      window.workflowAnimator.handleResize();
    }
  }, 250);
});

// Clean up on page unload
window.addEventListener('beforeunload', () => {
  if (window.workflowAnimator) {
    window.workflowAnimator.destroy();
  }
});

// Export for potential use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = WorkflowAnimator;
}