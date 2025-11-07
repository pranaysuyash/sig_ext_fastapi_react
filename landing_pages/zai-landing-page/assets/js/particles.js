/**
 * Particle System for Hero Section
 * Creates animated floating particles in the background
 */

class ParticleSystem {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    if (!this.container) {
      console.warn(`Particle container with id '${containerId}' not found`);
      return;
    }

    this.options = {
      particleCount: options.particleCount || 50,
      particleSize: options.particleSize || { min: 2, max: 6 },
      particleSpeed: options.particleSpeed || { min: 0.5, max: 2 },
      particleOpacity: options.particleOpacity || { min: 0.1, max: 0.8 },
      particleColor: options.particleColor || '#ffffff',
      connectionDistance: options.connectionDistance || 150,
      connectionOpacity: options.connectionOpacity || 0.2,
      mouseInteraction: options.mouseInteraction !== false,
      responsive: options.responsive !== false,
      performanceMode: options.performanceMode || 'auto', // 'auto', 'high', 'low'
      ...options
    };

    this.particles = [];
    this.animationId = null;
    this.mousePosition = { x: 0, y: 0 };
    this.isRunning = false;
    this.isVisible = true;

    this.init();
  }

  init() {
    this.setupCanvas();
    this.createParticles();
    this.setupEventListeners();
    this.start();
  }

  /**
   * Setup canvas element
   */
  setupCanvas() {
    this.canvas = document.createElement('canvas');
    this.canvas.className = 'particle-canvas';
    this.ctx = this.canvas.getContext('2d');

    // Set initial size
    this.resizeCanvas();

    // Add to container
    this.container.appendChild(this.canvas);
  }

  /**
   * Resize canvas to match container
   */
  resizeCanvas() {
    const rect = this.container.getBoundingClientRect();
    this.canvas.width = rect.width;
    this.canvas.height = rect.height;
  }

  /**
   * Create particle instances
   */
  createParticles() {
    this.particles = [];

    // Adjust particle count based on performance mode
    let particleCount = this.options.particleCount;

    if (this.options.performanceMode === 'low' ||
        (this.options.performanceMode === 'auto' && this.isLowPerformance())) {
      particleCount = Math.floor(particleCount * 0.5);
    }

    for (let i = 0; i < particleCount; i++) {
      this.particles.push(this.createParticle());
    }
  }

  /**
   * Create individual particle
   */
  createParticle() {
    const size = this.randomBetween(
      this.options.particleSize.min,
      this.options.particleSize.max
    );

    const speed = this.randomBetween(
      this.options.particleSpeed.min,
      this.options.particleSpeed.max
    );

    const opacity = this.randomBetween(
      this.options.particleOpacity.min,
      this.options.particleOpacity.max
    );

    return {
      x: Math.random() * this.canvas.width,
      y: Math.random() * this.canvas.height,
      vx: (Math.random() - 0.5) * speed,
      vy: (Math.random() - 0.5) * speed,
      size: size,
      opacity: opacity,
      originalOpacity: opacity,
      hue: Math.random() * 60 - 30 // -30 to +30 degrees for color variation
    };
  }

  /**
   * Setup event listeners
   */
  setupEventListeners() {
    // Window resize
    if (this.options.responsive) {
      window.addEventListener('resize', this.debounce(() => {
        this.resizeCanvas();
        this.redistributeParticles();
      }, 250));
    }

    // Mouse interaction
    if (this.options.mouseInteraction) {
      this.container.addEventListener('mousemove', (e) => {
        const rect = this.container.getBoundingClientRect();
        this.mousePosition = {
          x: e.clientX - rect.left,
          y: e.clientY - rect.top
        };
      });

      this.container.addEventListener('mouseleave', () => {
        this.mousePosition = { x: 0, y: 0 };
      });
    }

    // Visibility change
    document.addEventListener('visibilitychange', () => {
      this.isVisible = !document.hidden;
      if (this.isVisible && !this.isRunning) {
        this.start();
      } else if (!this.isVisible && this.isRunning) {
        this.pause();
      }
    });

    // Performance monitoring
    if (this.options.performanceMode === 'auto') {
      this.monitorPerformance();
    }
  }

  /**
   * Start the animation
   */
  start() {
    if (this.isRunning) return;

    this.isRunning = true;
    this.animate();
  }

  /**
   * Pause the animation
   */
  pause() {
    this.isRunning = false;
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }

  /**
   * Stop and destroy the particle system
   */
  destroy() {
    this.pause();

    // Remove event listeners
    window.removeEventListener('resize', this.resizeCanvas);
    this.container.removeEventListener('mousemove', this.updateMousePosition);

    // Remove canvas
    if (this.canvas && this.canvas.parentNode) {
      this.canvas.parentNode.removeChild(this.canvas);
    }

    this.particles = [];
  }

  /**
   * Main animation loop
   */
  animate() {
    if (!this.isRunning) return;

    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Update and draw particles
    this.updateParticles();
    this.drawParticles();

    // Draw connections
    if (this.options.connectionDistance > 0) {
      this.drawConnections();
    }

    this.animationId = requestAnimationFrame(() => this.animate());
  }

  /**
   * Update particle positions
   */
  updateParticles() {
    this.particles.forEach(particle => {
      // Update position
      particle.x += particle.vx;
      particle.y += particle.vy;

      // Mouse interaction
      if (this.options.mouseInteraction &&
          this.mousePosition.x > 0 &&
          this.mousePosition.y > 0) {
        const dx = this.mousePosition.x - particle.x;
        const dy = this.mousePosition.y - particle.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 100) {
          const force = (100 - distance) / 100;
          particle.vx -= (dx / distance) * force * 0.5;
          particle.vy -= (dy / distance) * force * 0.5;
        }
      }

      // Bounce off walls
      if (particle.x <= particle.size || particle.x >= this.canvas.width - particle.size) {
        particle.vx *= -1;
        particle.x = Math.max(particle.size, Math.min(this.canvas.width - particle.size, particle.x));
      }

      if (particle.y <= particle.size || particle.y >= this.canvas.height - particle.size) {
        particle.vy *= -1;
        particle.y = Math.max(particle.size, Math.min(this.canvas.height - particle.size, particle.y));
      }

      // Apply friction
      particle.vx *= 0.99;
      particle.vy *= 0.99;

      // Maintain minimum speed
      const minSpeed = this.options.particleSpeed.min * 0.5;
      const currentSpeed = Math.sqrt(particle.vx * particle.vx + particle.vy * particle.vy);
      if (currentSpeed < minSpeed) {
        const angle = Math.random() * Math.PI * 2;
        particle.vx = Math.cos(angle) * minSpeed;
        particle.vy = Math.sin(angle) * minSpeed;
      }
    });
  }

  /**
   * Draw particles
   */
  drawParticles() {
    this.particles.forEach(particle => {
      this.ctx.save();

      // Set particle style
      this.ctx.globalAlpha = particle.opacity;
      this.ctx.fillStyle = this.options.particleColor;

      // Add subtle color variation
      if (particle.hue !== 0) {
        this.ctx.filter = `hue-rotate(${particle.hue}deg)`;
      }

      // Draw particle
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
      this.ctx.fill();

      // Add glow effect for larger particles
      if (particle.size > 4) {
        this.ctx.globalAlpha = particle.opacity * 0.3;
        this.ctx.beginPath();
        this.ctx.arc(particle.x, particle.y, particle.size * 2, 0, Math.PI * 2);
        this.ctx.fill();
      }

      this.ctx.restore();
    });
  }

  /**
   * Draw connections between nearby particles
   */
  drawConnections() {
    const maxDistance = this.options.connectionDistance;
    const connectionOpacity = this.options.connectionOpacity;

    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const p1 = this.particles[i];
        const p2 = this.particles[j];

        const dx = p2.x - p1.x;
        const dy = p2.y - p1.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < maxDistance) {
          const opacity = (1 - distance / maxDistance) * connectionOpacity;

          this.ctx.save();
          this.ctx.globalAlpha = opacity * Math.min(p1.opacity, p2.opacity);
          this.ctx.strokeStyle = this.options.particleColor;
          this.ctx.lineWidth = 1;

          this.ctx.beginPath();
          this.ctx.moveTo(p1.x, p1.y);
          this.ctx.lineTo(p2.x, p2.y);
          this.ctx.stroke();

          this.ctx.restore();
        }
      }
    }
  }

  /**
   * Redistribute particles when canvas is resized
   */
  redistributeParticles() {
    this.particles.forEach(particle => {
      // Keep particles within new bounds
      particle.x = Math.min(particle.x, this.canvas.width - particle.size);
      particle.y = Math.min(particle.y, this.canvas.height - particle.size);
    });
  }

  /**
   * Check for low performance device
   */
  isLowPerformance() {
    // Simple heuristic for performance detection
    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');

    if (!gl) {
      return true; // No WebGL support
    }

    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
    if (debugInfo) {
      const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
      // Check for common low-performance indicators
      return /Mali|Adreno 3|PowerVR SGX|Intel|Microsoft/.test(renderer);
    }

    return false;
  }

  /**
   * Monitor performance and adjust quality
   */
  monitorPerformance() {
    let frameCount = 0;
    let lastTime = performance.now();
    let fps = 60;

    const checkPerformance = () => {
      frameCount++;
      const currentTime = performance.now();

      if (currentTime - lastTime >= 1000) {
        fps = frameCount;
        frameCount = 0;
        lastTime = currentTime;

        // Adjust quality based on performance
        if (fps < 30 && this.particles.length > 20) {
          // Reduce particle count
          const toRemove = Math.floor(this.particles.length * 0.3);
          this.particles.splice(0, toRemove);
        }
      }

      if (this.isRunning) {
        requestAnimationFrame(checkPerformance);
      }
    };

    requestAnimationFrame(checkPerformance);
  }

  /**
   * Utility: Get random number between min and max
   */
  randomBetween(min, max) {
    return Math.random() * (max - min) + min;
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
   * Get current performance metrics
   */
  getMetrics() {
    return {
      particleCount: this.particles.length,
      isRunning: this.isRunning,
      canvasSize: {
        width: this.canvas.width,
        height: this.canvas.height
      },
      performanceMode: this.options.performanceMode
    };
  }

  /**
   * Update options at runtime
   */
  updateOptions(newOptions) {
    this.options = { ...this.options, ...newOptions };

    // Recreate particles if count changed
    if (newOptions.particleCount && newOptions.particleCount !== this.particles.length) {
      this.createParticles();
    }
  }
}

// Auto-initialize particle system for hero section
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    const heroParticles = document.getElementById('particles-canvas');
    if (heroParticles) {
      window.particleSystem = new ParticleSystem('particles-canvas', {
        particleCount: window.innerWidth < 768 ? 20 : 50,
        particleSize: { min: 1, max: 3 },
        particleSpeed: { min: 0.3, max: 1.5 },
        particleOpacity: { min: 0.1, max: 0.6 },
        connectionDistance: 100,
        connectionOpacity: 0.15,
        mouseInteraction: true,
        responsive: true,
        performanceMode: 'auto'
      });
    }
  }, 100);
});

// Handle page visibility
document.addEventListener('visibilitychange', () => {
  if (window.particleSystem) {
    if (document.hidden) {
      window.particleSystem.pause();
    } else {
      window.particleSystem.start();
    }
  }
});

// Clean up on page unload
window.addEventListener('beforeunload', () => {
  if (window.particleSystem) {
    window.particleSystem.destroy();
  }
});

// Export for potential use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ParticleSystem;
}