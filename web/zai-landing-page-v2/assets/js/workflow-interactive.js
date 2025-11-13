/**
 * Interactive Workflow Animation for Signature Extractor
 * Advanced 6-step workflow with sophisticated animations and interactions
 */

class InteractiveWorkflow {
  constructor() {
    this.container = document.getElementById('workflow-container');
    this.steps = [
      {
        id: 'upload',
        title: 'Upload Document',
        description: 'Drag & drop or browse your PDF, image, or scan',
        icon: 'upload',
        color: '#00ff88',
        duration: 2000
      },
      {
        id: 'analyze',
        title: 'AI Analysis',
        description: 'Advanced AI scans for signature patterns and metadata',
        icon: 'brain',
        color: '#00d4ff',
        duration: 2500
      },
      {
        id: 'detect',
        title: 'Smart Detection',
        description: 'Locates and highlights all signature instances',
        icon: 'search',
        color: '#7b2ff7',
        duration: 2200
      },
      {
        id: 'extract',
        title: 'Clean Extraction',
        description: 'Precisely extracts signatures with quality preservation',
        icon: 'scissors',
        color: '#ff6b6b',
        duration: 1800
      },
      {
        id: 'enhance',
        title: 'Auto Enhancement',
        description: 'Improves clarity, contrast, and overall quality',
        icon: 'magic',
        color: '#ffd93d',
        duration: 2000
      },
      {
        id: 'export',
        title: 'Export Results',
        description: 'Download in multiple formats with batch processing',
        icon: 'download',
        color: '#00ff88',
        duration: 1500
      }
    ];

    this.currentStep = 0;
    this.isAutoPlaying = true;
    this.animationTimeout = null;
    this.stepElements = [];
    this.particleSystems = {};
    this.animations = {};
    this.progressPath = null;
    this.progressPointer = null;

    // Configuration
    this.config = {
      autoPlayDelay: 3000,
      transitionDuration: 800,
      particleCount: 20,
      enableSound: false,
      reducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
      touchOptimized: 'ontouchstart' in window
    };

    this.init();
  }

  init() {
    this.createWorkflowHTML();
    this.setupElements();
    this.createParticleSystems();
    this.bindEvents();
    this.createProgressPath();
    this.startAutoPlay();
    this.createAnimations();
  }

  createWorkflowHTML() {
    if (!this.container) return;

    const workflowHTML = `
      <div class="workflow-interactive">
        <div class="workflow-header">
          <h2 class="workflow-title">How It Works</h2>
          <p class="workflow-subtitle">Experience the magic of AI-powered signature extraction</p>
          <div class="workflow-controls">
            <button class="workflow-btn" id="play-pause-btn" aria-label="Play/Pause">
              <svg class="icon-play" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z"/>
              </svg>
              <svg class="icon-pause" viewBox="0 0 24 24">
                <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
              </svg>
            </button>
            <button class="workflow-btn" id="prev-btn" aria-label="Previous Step">
              <svg viewBox="0 0 24 24">
                <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
              </svg>
            </button>
            <button class="workflow-btn" id="next-btn" aria-label="Next Step">
              <svg viewBox="0 0 24 24">
                <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
              </svg>
            </button>
          </div>
        </div>

        <div class="workflow-progress">
          <svg class="progress-svg" viewBox="0 0 1200 100">
            <defs>
              <linearGradient id="progress-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#00ff88;stop-opacity:0.3" />
                <stop offset="50%" style="stop-color:#00d4ff;stop-opacity:0.3" />
                <stop offset="100%" style="stop-color:#7b2ff7;stop-opacity:0.3" />
              </linearGradient>
            </defs>
            <path class="progress-track" d="M 100 50 Q 300 20, 500 50 T 900 50 T 1100 50" />
            <path class="progress-fill" d="M 100 50 Q 300 20, 500 50 T 900 50 T 1100 50" />
          </svg>
          <div class="progress-pointer" id="progress-pointer"></div>
        </div>

        <div class="workflow-steps">
          ${this.steps.map((step, index) => `
            <div class="workflow-step" data-step="${index}" data-id="${step.id}">
              <div class="step-visual">
                <div class="step-icon-container">
                  <div class="step-icon">
                    ${this.createStepIcon(step.icon)}
                  </div>
                  <div class="step-particles" id="particles-${step.id}"></div>
                </div>
                <div class="step-number">${index + 1}</div>
              </div>
              <div class="step-content">
                <h3 class="step-title">${step.title}</h3>
                <p class="step-description">${step.description}</p>
                <div class="step-status">
                  <span class="status-text"></span>
                  <div class="status-progress">
                    <div class="progress-bar"></div>
                  </div>
                </div>
              </div>
              <div class="step-visualization">
                ${this.createStepVisualization(step)}
              </div>
            </div>
          `).join('')}
        </div>

        <div class="workflow-indicators">
          ${this.steps.map((step, index) => `
            <button class="step-indicator" data-step="${index}" aria-label="Go to step ${index + 1}">
              <span class="indicator-dot"></span>
              <span class="indicator-label">${step.title}</span>
            </button>
          `).join('')}
        </div>
      </div>
    `;

    this.container.innerHTML = workflowHTML;
  }

  createStepIcon(iconType) {
    const icons = {
      upload: '<svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>',
      brain: '<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/></svg>',
      search: '<svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>',
      scissors: '<svg viewBox="0 0 24 24"><path d="M9.64 7.64c.23-.5.36-1.05.36-1.64 0-2.21-1.79-4-4-4S2 3.79 2 6s1.79 4 4 4c.59 0 1.14-.13 1.64-.36L10 12l-2.36 2.36C7.14 14.13 6.59 14 6 14c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4c0-.59-.13-1.14-.36-1.64L12 14l7 7h3v-1L9.64 7.64zM6 8c-1.1 0-2-.89-2-2s.9-2 2-2 2 .89 2 2-.9 2-2 2zm0 12c-1.1 0-2-.89-2-2s.9-2 2-2 2 .89 2 2-.9 2-2 2zm6-7.5c-.28 0-.5-.22-.5-.5s.22-.5.5-.5.5.22.5.5-.22.5-.5.5zM19 3l-6 6 2 2 7-7V3z"/></svg>',
      magic: '<svg viewBox="0 0 24 24"><path d="M7.5 5.6L10 7 8.6 4.5 10 2 7.5 3.4 5 2l1.4 2.5L5 7l2.5-1.4L10 7 8.6 4.5zm12 9.8L17 14l1.4 2.5L17 19l2.5-1.4L22 19l-1.4-2.5L22 14l-2.5 1.4zm-7.5-7.5L9 9l1.4 2.5L9 14l2.5-1.4L14 14l-1.4-2.5L14 9l-2.5 1.4z"/></svg>',
      download: '<svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>'
    };
    return icons[iconType] || icons.upload;
  }

  createStepVisualization(step) {
    const visualizations = {
      upload: `
        <div class="upload-visualization">
          <div class="upload-area">
            <div class="upload-documents">
              <div class="doc doc-1"></div>
              <div class="doc doc-2"></div>
              <div class="doc doc-3"></div>
            </div>
            <div class="upload-arrow"></div>
          </div>
        </div>
      `,
      analyze: `
        <div class="analyze-visualization">
          <div class="brain-core"></div>
          <div class="brain-waves">
            <div class="wave wave-1"></div>
            <div class="wave wave-2"></div>
            <div class="wave wave-3"></div>
          </div>
          <div class="data-points"></div>
        </div>
      `,
      detect: `
        <div class="detect-visualization">
          <div class="document-preview">
            <div class="sig-candidate sig-1"></div>
            <div class="sig-candidate sig-2"></div>
            <div class="sig-candidate sig-3"></div>
          </div>
          <div class="scan-line"></div>
        </div>
      `,
      extract: `
        <div class="extract-visualization">
          <div class="source-doc"></div>
          <div class="extraction-beam"></div>
          <div class="extracted-sig"></div>
        </div>
      `,
      enhance: `
        <div class="enhance-visualization">
          <div class="enhance-sliders">
            <div class="slider slider-contrast"></div>
            <div class="slider slider-brightness"></div>
            <div class="slider slider-sharpness"></div>
          </div>
          <div class="enhance-preview"></div>
        </div>
      `,
      export: `
        <div class="export-visualization">
          <div class="export-formats">
            <div class="format format-pdf">PDF</div>
            <div class="format format-png">PNG</div>
            <div class="format format-svg">SVG</div>
          </div>
          <div class="export-arrows"></div>
        </div>
      `
    };

    return visualizations[step.id] || '<div class="default-visualization"></div>';
  }

  setupElements() {
    this.stepElements = this.container.querySelectorAll('.workflow-step');
    this.progressPath = this.container.querySelector('.progress-fill');
    this.progressPointer = this.container.getElementById('progress-pointer');
    this.playPauseBtn = this.container.getElementById('play-pause-btn');
    this.prevBtn = this.container.getElementById('prev-btn');
    this.nextBtn = this.container.getElementById('next-btn');
    this.indicators = this.container.querySelectorAll('.step-indicator');
  }

  createParticleSystems() {
    this.steps.forEach(step => {
      const container = document.getElementById(`particles-${step.id}`);
      if (container) {
        this.particleSystems[step.id] = this.createMiniParticleSystem(container, step.color);
      }
    });
  }

  createMiniParticleSystem(container, color) {
    const particles = [];
    const particleCount = 15;

    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div');
      particle.className = 'mini-particle';
      particle.style.cssText = `
        position: absolute;
        width: 3px;
        height: 3px;
        background: ${color};
        border-radius: 50%;
        opacity: 0;
        pointer-events: none;
      `;
      container.appendChild(particle);

      particles.push({
        element: particle,
        x: Math.random() * 100,
        y: Math.random() * 100,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
        life: 1,
        delay: Math.random() * 1000
      });
    }

    return { particles, active: false };
  }

  bindEvents() {
    // Control buttons
    if (this.playPauseBtn) {
      this.playPauseBtn.addEventListener('click', () => this.toggleAutoPlay());
    }

    if (this.prevBtn) {
      this.prevBtn.addEventListener('click', () => this.previousStep());
    }

    if (this.nextBtn) {
      this.nextBtn.addEventListener('click', () => this.nextStep());
    }

    // Step indicators
    this.indicators.forEach((indicator, index) => {
      indicator.addEventListener('click', () => this.goToStep(index));
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      switch (e.key) {
        case 'ArrowLeft':
          this.previousStep();
          break;
        case 'ArrowRight':
          this.nextStep();
          break;
        case ' ':
          e.preventDefault();
          this.toggleAutoPlay();
          break;
        case 'Home':
          this.goToStep(0);
          break;
        case 'End':
          this.goToStep(this.steps.length - 1);
          break;
      }
    });

    // Touch gestures
    if (this.config.touchOptimized) {
      this.bindTouchGestures();
    }

    // Visibility change
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        this.pauseAutoPlay();
      } else if (this.isAutoPlaying) {
        this.startAutoPlay();
      }
    });
  }

  bindTouchGestures() {
    let startX = 0;
    let startY = 0;

    this.container.addEventListener('touchstart', (e) => {
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
    });

    this.container.addEventListener('touchend', (e) => {
      const endX = e.changedTouches[0].clientX;
      const endY = e.changedTouches[0].clientY;
      const diffX = endX - startX;
      const diffY = endY - startY;

      if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
        if (diffX > 0) {
          this.nextStep();
        } else {
          this.previousStep();
        }
      }
    });
  }

  createProgressPath() {
    if (!this.progressPath) return;

    const pathLength = this.progressPath.getTotalLength();
    this.progressPath.style.strokeDasharray = pathLength;
    this.progressPath.style.strokeDashoffset = pathLength;
  }

  createAnimations() {
    // Step entrance animations
    this.steps.forEach((step, index) => {
      const stepElement = this.stepElements[index];
      if (stepElement) {
        this.animations[step.id] = {
          entrance: this.createStepEntranceAnimation(stepElement, index),
          active: this.createStepActiveAnimation(stepElement, step),
          exit: this.createStepExitAnimation(stepElement, index)
        };
      }
    });
  }

  createStepEntranceAnimation(element, index) {
    return {
      duration: this.config.transitionDuration,
      delay: index * 100,
      easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
    };
  }

  createStepActiveAnimation(element, step) {
    return {
      duration: step.duration,
      particles: this.particleSystems[step.id],
      visualization: element.querySelector('.step-visualization')
    };
  }

  createStepExitAnimation(element, index) {
    return {
      duration: 600,
      easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
    };
  }

  startAutoPlay() {
    if (!this.isAutoPlaying) return;

    this.clearAutoPlayTimeout();
    this.animationTimeout = setTimeout(() => {
      this.nextStep();
      this.startAutoPlay();
    }, this.config.autoPlayDelay);
  }

  pauseAutoPlay() {
    this.clearAutoPlayTimeout();
  }

  clearAutoPlayTimeout() {
    if (this.animationTimeout) {
      clearTimeout(this.animationTimeout);
      this.animationTimeout = null;
    }
  }

  toggleAutoPlay() {
    this.isAutoPlaying = !this.isAutoPlaying;

    if (this.isAutoPlaying) {
      this.playPauseBtn.classList.add('playing');
      this.startAutoPlay();
    } else {
      this.playPauseBtn.classList.remove('playing');
      this.pauseAutoPlay();
    }
  }

  nextStep() {
    const nextIndex = (this.currentStep + 1) % this.steps.length;
    this.goToStep(nextIndex);
  }

  previousStep() {
    const prevIndex = this.currentStep === 0 ? this.steps.length - 1 : this.currentStep - 1;
    this.goToStep(prevIndex);
  }

  goToStep(index) {
    if (index === this.currentStep || index < 0 || index >= this.steps.length) return;

    const prevStep = this.currentStep;
    this.currentStep = index;

    // Update UI
    this.updateSteps(prevStep, index);
    this.updateProgress();
    this.updateIndicators();
    this.updateVisualization(index);

    // Announce for screen readers
    this.announceStepChange(index);

    // Restart auto-play if enabled
    if (this.isAutoPlaying) {
      this.startAutoPlay();
    }
  }

  updateSteps(prevIndex, currentIndex) {
    // Exit previous step
    if (this.stepElements[prevIndex]) {
      this.stepElements[prevIndex].classList.remove('active', 'completed');
      this.stopStepAnimation(this.steps[prevIndex].id);
    }

    // Activate current step
    if (this.stepElements[currentIndex]) {
      this.stepElements[currentIndex].classList.add('active');
      this.stepElements[currentIndex].classList.remove('completed');
      this.startStepAnimation(this.steps[currentIndex].id);

      // Mark previous steps as completed
      for (let i = 0; i < currentIndex; i++) {
        if (this.stepElements[i]) {
          this.stepElements[i].classList.add('completed');
        }
      }
    }
  }

  updateProgress() {
    if (!this.progressPath) return;

    const pathLength = this.progressPath.getTotalLength();
    const progress = this.currentStep / (this.steps.length - 1);
    const offset = pathLength - (progress * pathLength);

    if (!this.config.reducedMotion) {
      this.progressPath.style.transition = `stroke-dashoffset ${this.config.transitionDuration}ms cubic-bezier(0.4, 0, 0.2, 1)`;
    }
    this.progressPath.style.strokeDashoffset = offset;

    // Update progress pointer position
    if (this.progressPointer) {
      const percentage = (this.currentStep / (this.steps.length - 1)) * 100;
      this.progressPointer.style.left = `${percentage}%`;
    }
  }

  updateIndicators() {
    this.indicators.forEach((indicator, index) => {
      indicator.classList.toggle('active', index === this.currentStep);
      indicator.classList.toggle('completed', index < this.currentStep);
      indicator.setAttribute('aria-current', index === this.currentStep ? 'step' : 'false');
    });
  }

  updateVisualization(index) {
    const step = this.steps[index];
    const stepElement = this.stepElements[index];
    const visualization = stepElement?.querySelector('.step-visualization');

    if (visualization) {
      // Trigger visualization-specific animations
      this.triggerVisualizationAnimation(step.id, visualization);
    }
  }

  triggerVisualizationAnimation(stepId, visualization) {
    switch (stepId) {
      case 'upload':
        this.animateUpload(visualization);
        break;
      case 'analyze':
        this.animateAnalyze(visualization);
        break;
      case 'detect':
        this.animateDetect(visualization);
        break;
      case 'extract':
        this.animateExtract(visualization);
        break;
      case 'enhance':
        this.animateEnhance(visualization);
        break;
      case 'export':
        this.animateExport(visualization);
        break;
    }
  }

  animateUpload(visualization) {
    const docs = visualization.querySelectorAll('.doc');
    const arrow = visualization.querySelector('.upload-arrow');

    docs.forEach((doc, index) => {
      doc.style.animation = `slideUp 0.6s ease-out ${index * 0.1}s both`;
    });

    if (arrow) {
      setTimeout(() => {
        arrow.style.animation = 'pulse 1s ease-in-out infinite';
      }, 600);
    }
  }

  animateAnalyze(visualization) {
    const waves = visualization.querySelectorAll('.wave');
    const core = visualization.querySelector('.brain-core');

    if (core) {
      core.style.animation = 'pulse 2s ease-in-out infinite';
    }

    waves.forEach((wave, index) => {
      wave.style.animation = `ripple 1.5s ease-out ${index * 0.2}s infinite`;
    });
  }

  animateDetect(visualization) {
    const scanLine = visualization.querySelector('.scan-line');
    const candidates = visualization.querySelectorAll('.sig-candidate');

    if (scanLine) {
      scanLine.style.animation = 'scan 2s ease-in-out infinite';
    }

    candidates.forEach((candidate, index) => {
      setTimeout(() => {
        candidate.style.animation = 'glow 0.8s ease-out both';
      }, 500 + index * 300);
    });
  }

  animateExtract(visualization) {
    const beam = visualization.querySelector('.extraction-beam');
    const extracted = visualization.querySelector('.extracted-sig');

    if (beam) {
      beam.style.animation = 'beam 1.5s ease-in-out both';
    }

    if (extracted) {
      setTimeout(() => {
        extracted.style.animation = 'fadeInScale 0.8s ease-out both';
      }, 800);
    }
  }

  animateEnhance(visualization) {
    const sliders = visualization.querySelectorAll('.slider');
    const preview = visualization.querySelector('.enhance-preview');

    sliders.forEach((slider, index) => {
      setTimeout(() => {
        slider.style.animation = 'sliderMove 1s ease-in-out both';
      }, index * 200);
    });

    if (preview) {
      setTimeout(() => {
        preview.style.animation = 'enhanceGlow 2s ease-in-out infinite';
      }, 800);
    }
  }

  animateExport(visualization) {
    const formats = visualization.querySelectorAll('.format');
    const arrows = visualization.querySelector('.export-arrows');

    formats.forEach((format, index) => {
      setTimeout(() => {
        format.style.animation = 'popIn 0.5s ease-out both';
      }, index * 150);
    });

    if (arrows) {
      setTimeout(() => {
        arrows.style.animation = 'arrowsFly 1.5s ease-in-out infinite';
      }, 800);
    }
  }

  startStepAnimation(stepId) {
    const particleSystem = this.particleSystems[stepId];
    if (particleSystem) {
      particleSystem.active = true;
      this.animateParticles(particleSystem);
    }
  }

  stopStepAnimation(stepId) {
    const particleSystem = this.particleSystems[stepId];
    if (particleSystem) {
      particleSystem.active = false;
    }
  }

  animateParticles(particleSystem) {
    if (!particleSystem.active) return;

    particleSystem.particles.forEach(particle => {
      setTimeout(() => {
        if (particleSystem.active) {
          this.animateParticle(particle);
        }
      }, particle.delay);
    });

    if (particleSystem.active) {
      requestAnimationFrame(() => this.animateParticles(particleSystem));
    }
  }

  animateParticle(particle) {
    particle.x += particle.vx;
    particle.y += particle.vy;
    particle.life -= 0.02;

    if (particle.life <= 0) {
      // Reset particle
      particle.x = Math.random() * 100;
      particle.y = Math.random() * 100;
      particle.life = 1;
    }

    const opacity = particle.life * 0.8;
    particle.element.style.opacity = opacity;
    particle.element.style.transform = `translate(${particle.x}%, ${particle.y}%)`;
  }

  announceStepChange(index) {
    const step = this.steps[index];
    const announcement = `Step ${index + 1} of ${this.steps.length}: ${step.title}. ${step.description}`;

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

  // Public API
  getCurrentStep() {
    return this.currentStep;
  }

  getStepData(index) {
    return this.steps[index] || null;
  }

  setAutoPlayDelay(delay) {
    this.config.autoPlayDelay = delay;
  }

  destroy() {
    this.pauseAutoPlay();

    // Clean up particle systems
    Object.values(this.particleSystems).forEach(system => {
      system.particles.forEach(particle => {
        particle.element.remove();
      });
    });

    // Remove event listeners
    // (Implementation depends on how they were added)
  }
}

// Initialize workflow when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const workflowContainer = document.getElementById('workflow-container');
  if (workflowContainer) {
    window.interactiveWorkflow = new InteractiveWorkflow();
  }
});

// Make available globally for non-module usage
window.InteractiveWorkflow = InteractiveWorkflow;