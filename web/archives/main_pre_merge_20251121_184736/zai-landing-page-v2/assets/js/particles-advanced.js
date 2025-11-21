/**
 * Advanced Particle System for Signature Extractor
 * Sophisticated particle effects with mouse interaction and performance optimization
 */

class AdvancedParticleSystem {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.canvas = document.createElement('canvas');
    this.ctx = this.canvas.getContext('2d');

    // Configuration
    this.config = {
      particleCount: 30,
      connectionDistance: 150,
      mouseInteractionRadius: 200,
      particleSpeed: { min: 0.2, max: 1.5 },
      particleSize: { min: 0.5, max: 2 },
      colors: ['rgba(0, 102, 204, 0.3)', 'rgba(44, 62, 80, 0.3)', 'rgba(52, 73, 94, 0.2)'],
      backgroundOpacity: 0.03,
      glowIntensity: 0.1,
      performanceMode: 'auto', // 'high', 'medium', 'low', 'auto'
      adaptiveQuality: true,
      mouseForce: 0.3,
      connectionOpacity: 0.15,
      pulseSpeed: 0.002,
      ...options
    };

    // State
    this.particles = [];
    this.mouse = { x: 0, y: 0, isActive: false };
    this.raf = null;
    this.isRunning = false;
    this.performanceMetrics = {
      fps: 60,
      frameTime: 0,
      lastTime: performance.now(),
      adaptiveLevel: 'high'
    };
    this.bounds = { width: 0, height: 0 };

    this.init();
  }

  init() {
    this.setupCanvas();
    this.createParticles();
    this.bindEvents();
    this.start();
  }

  setupCanvas() {
    this.canvas.style.position = 'absolute';
    this.canvas.style.top = '0';
    this.canvas.style.left = '0';
    this.canvas.style.width = '100%';
    this.canvas.style.height = '100%';
    this.canvas.style.pointerEvents = 'none';
    this.canvas.style.zIndex = '1';

    this.container.appendChild(this.canvas);
    this.updateBounds();
  }

  updateBounds() {
    const rect = this.container.getBoundingClientRect();
    this.bounds = {
      width: rect.width,
      height: rect.height
    };

    this.canvas.width = this.bounds.width * window.devicePixelRatio;
    this.canvas.height = this.bounds.height * window.devicePixelRatio;
    this.ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  }

  createParticles() {
    this.particles = [];

    for (let i = 0; i < this.config.particleCount; i++) {
      this.particles.push(this.createParticle());
    }
  }

  createParticle(x = null, y = null, type = 'normal') {
    const speed = this.config.particleSpeed;
    const size = this.config.particleSize;

    return {
      x: x !== null ? x : Math.random() * this.bounds.width,
      y: y !== null ? y : Math.random() * this.bounds.height,
      vx: (Math.random() - 0.5) * (speed.max - speed.min) + speed.min,
      vy: (Math.random() - 0.5) * (speed.max - speed.min) + speed.min,
      radius: Math.random() * (size.max - size.min) + size.min,
      color: this.config.colors[Math.floor(Math.random() * this.config.colors.length)],
      alpha: Math.random() * 0.5 + 0.5,
      pulsePhase: Math.random() * Math.PI * 2,
      pulseSpeed: this.config.pulseSpeed * (0.5 + Math.random()),
      type: type,
      life: 1,
      maxLife: type === 'temporary' ? 60 + Math.random() * 60 : Infinity,
      orbit: {
        center: {
          x: this.bounds.width / 2,
          y: this.bounds.height / 2
        },
        radius: Math.random() * 100 + 50,
        angle: Math.random() * Math.PI * 2,
        speed: (Math.random() - 0.5) * 0.01
      },
      connections: [],
      trail: [],
      maxTrailLength: 5
    };
  }

  bindEvents() {
    // Mouse events
    this.container.addEventListener('mousemove', (e) => this.handleMouseMove(e));
    this.container.addEventListener('mouseenter', () => this.handleMouseEnter());
    this.container.addEventListener('mouseleave', () => this.handleMouseLeave());

    // Touch events
    this.container.addEventListener('touchstart', (e) => this.handleTouchStart(e));
    this.container.addEventListener('touchmove', (e) => this.handleTouchMove(e));
    this.container.addEventListener('touchend', () => this.handleTouchEnd());

    // Window events
    window.addEventListener('resize', () => this.handleResize());
    window.addEventListener('visibilitychange', () => this.handleVisibilityChange());

    // Performance monitoring
    if (this.config.adaptiveQuality) {
      this.monitorPerformance();
    }
  }

  handleMouseMove(e) {
    const rect = this.container.getBoundingClientRect();
    this.mouse.x = e.clientX - rect.left;
    this.mouse.y = e.clientY - rect.top;
    this.mouse.isActive = true;
  }

  handleMouseEnter() {
    this.mouse.isActive = true;
  }

  handleMouseLeave() {
    this.mouse.isActive = false;
  }

  handleTouchStart(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const rect = this.container.getBoundingClientRect();
    this.mouse.x = touch.clientX - rect.left;
    this.mouse.y = touch.clientY - rect.top;
    this.mouse.isActive = true;
  }

  handleTouchMove(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const rect = this.container.getBoundingClientRect();
    this.mouse.x = touch.clientX - rect.left;
    this.mouse.y = touch.clientY - rect.top;
  }

  handleTouchEnd() {
    this.mouse.isActive = false;
  }

  handleResize() {
    this.updateBounds();
  }

  handleVisibilityChange() {
    if (document.hidden) {
      this.pause();
    } else {
      this.start();
    }
  }

  start() {
    if (this.isRunning) return;
    this.isRunning = true;
    this.animate();
  }

  pause() {
    this.isRunning = false;
    if (this.raf) {
      cancelAnimationFrame(this.raf);
      this.raf = null;
    }
  }

  animate() {
    if (!this.isRunning) return;

    this.update();
    this.draw();

    this.raf = requestAnimationFrame(() => this.animate());
  }

  update() {
    // Update performance metrics
    this.updatePerformanceMetrics();

    // Update particles
    this.updateParticles();

    // Update connections
    this.updateConnections();

    // Adapt quality if needed
    if (this.config.adaptiveQuality) {
      this.adaptQuality();
    }
  }

  updateParticles() {
    this.particles = this.particles.filter(particle => {
      // Update life
      if (particle.type === 'temporary') {
        particle.life -= 1 / particle.maxLife;
        if (particle.life <= 0) return false;
      }

      // Store trail position
      if (particle.trail) {
        particle.trail.push({ x: particle.x, y: particle.y, alpha: particle.alpha });
        if (particle.trail.length > particle.maxTrailLength) {
          particle.trail.shift();
        }
      }

      // Update position based on type
      switch (particle.type) {
        case 'normal':
          this.updateNormalParticle(particle);
          break;
        case 'orbit':
          this.updateOrbitParticle(particle);
          break;
        case 'mouse':
          this.updateMouseParticle(particle);
          break;
        case 'temporary':
          this.updateTemporaryParticle(particle);
          break;
      }

      // Update pulse
      particle.pulsePhase += particle.pulseSpeed;

      // Mouse interaction
      if (this.mouse.isActive) {
        this.applyMouseForce(particle);
      }

      // Boundary check
      this.checkBoundaries(particle);

      return true;
    });

    // Maintain particle count
    const targetCount = this.getAdaptiveParticleCount();
    while (this.particles.length < targetCount) {
      this.particles.push(this.createParticle());
    }
  }

  updateNormalParticle(particle) {
    particle.x += particle.vx;
    particle.y += particle.vy;

    // Add some randomness
    particle.vx += (Math.random() - 0.5) * 0.01;
    particle.vy += (Math.random() - 0.5) * 0.01;

    // Limit speed
    const speed = Math.sqrt(particle.vx * particle.vx + particle.vy * particle.vy);
    const maxSpeed = 2;
    if (speed > maxSpeed) {
      particle.vx = (particle.vx / speed) * maxSpeed;
      particle.vy = (particle.vy / speed) * maxSpeed;
    }
  }

  updateOrbitParticle(particle) {
    particle.orbit.angle += particle.orbit.speed;
    particle.x = particle.orbit.center.x + Math.cos(particle.orbit.angle) * particle.orbit.radius;
    particle.y = particle.orbit.center.y + Math.sin(particle.orbit.angle) * particle.orbit.radius;

    // Slowly change orbit radius
    particle.orbit.radius += Math.sin(particle.pulsePhase) * 0.5;
  }

  updateMouseParticle(particle) {
    if (this.mouse.isActive) {
      const dx = this.mouse.x - particle.x;
      const dy = this.mouse.y - particle.y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance > 10) {
        particle.vx += (dx / distance) * 0.1;
        particle.vy += (dy / distance) * 0.1;
      }
    }

    particle.x += particle.vx;
    particle.y += particle.vy;
    particle.vx *= 0.95;
    particle.vy *= 0.95;
  }

  updateTemporaryParticle(particle) {
    particle.x += particle.vx;
    particle.y += particle.vy;
    particle.vy += 0.1; // Gravity effect
    particle.vx *= 0.98;
    particle.vy *= 0.98;
    particle.alpha = particle.life * 0.8;
  }

  applyMouseForce(particle) {
    const dx = this.mouse.x - particle.x;
    const dy = this.mouse.y - particle.y;
    const distance = Math.sqrt(dx * dx + dy * dy);

    if (distance < this.config.mouseInteractionRadius) {
      const force = (1 - distance / this.config.mouseInteractionRadius) * this.config.mouseForce;

      if (particle.type === 'mouse') {
        // Attract to mouse
        particle.vx += (dx / distance) * force;
        particle.vy += (dy / distance) * force;
      } else {
        // Repel from mouse
        particle.vx -= (dx / distance) * force * 0.5;
        particle.vy -= (dy / distance) * force * 0.5;
      }
    }
  }

  checkBoundaries(particle) {
    const margin = 50;

    if (particle.x < -margin) {
      particle.x = this.bounds.width + margin;
    } else if (particle.x > this.bounds.width + margin) {
      particle.x = -margin;
    }

    if (particle.y < -margin) {
      particle.y = this.bounds.height + margin;
    } else if (particle.y > this.bounds.height + margin) {
      particle.y = -margin;
    }
  }

  updateConnections() {
    // Clear existing connections
    this.particles.forEach(particle => {
      particle.connections = [];
    });

    // Find connections between nearby particles
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const p1 = this.particles[i];
        const p2 = this.particles[j];

        const dx = p1.x - p2.x;
        const dy = p1.y - p2.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < this.config.connectionDistance) {
          const opacity = (1 - distance / this.config.connectionDistance) * this.config.connectionOpacity;

          p1.connections.push({
            particle: p2,
            distance: distance,
            opacity: opacity
          });
        }
      }
    }
  }

  draw() {
    // Clear canvas with trail effect
    this.ctx.fillStyle = `rgba(7, 9, 16, ${this.config.backgroundOpacity})`;
    this.ctx.fillRect(0, 0, this.bounds.width, this.bounds.height);

    // Draw connections
    this.drawConnections();

    // Draw particles
    this.drawParticles();
  }

  drawConnections() {
    this.particles.forEach(particle => {
      particle.connections.forEach(connection => {
        this.ctx.save();

        this.ctx.globalAlpha = connection.opacity * particle.life;
        this.ctx.strokeStyle = connection.particle.color;
        this.ctx.lineWidth = 0.5;

        // Add glow effect
        this.ctx.shadowBlur = 5;
        this.ctx.shadowColor = connection.particle.color;

        this.ctx.beginPath();
        this.ctx.moveTo(particle.x, particle.y);
        this.ctx.lineTo(connection.particle.x, connection.particle.y);
        this.ctx.stroke();

        this.ctx.restore();
      });
    });
  }

  drawParticles() {
    this.particles.forEach(particle => {
      this.ctx.save();

      // Calculate pulse effect
      const pulseFactor = 1 + Math.sin(particle.pulsePhase) * 0.2;
      const currentRadius = particle.radius * pulseFactor;

      // Draw trail
      if (particle.trail && particle.trail.length > 1) {
        this.drawTrail(particle);
      }

      // Set glow effect
      this.ctx.shadowBlur = 10 * this.config.glowIntensity;
      this.ctx.shadowColor = particle.color;

      // Draw particle
      this.ctx.globalAlpha = particle.alpha * particle.life;
      this.ctx.fillStyle = particle.color;

      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, currentRadius, 0, Math.PI * 2);
      this.ctx.fill();

      // Draw inner glow
      this.ctx.globalAlpha = particle.alpha * particle.life * 0.5;
      this.ctx.fillStyle = '#ffffff';

      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, currentRadius * 0.3, 0, Math.PI * 2);
      this.ctx.fill();

      this.ctx.restore();
    });
  }

  drawTrail(particle) {
    if (particle.trail.length < 2) return;

    this.ctx.save();
    this.ctx.lineCap = 'round';
    this.ctx.lineJoin = 'round';

    for (let i = 1; i < particle.trail.length; i++) {
      const prev = particle.trail[i - 1];
      const curr = particle.trail[i];

      this.ctx.globalAlpha = (i / particle.trail.length) * particle.life * 0.3;
      this.ctx.strokeStyle = particle.color;
      this.ctx.lineWidth = particle.radius * 0.5;

      this.ctx.beginPath();
      this.ctx.moveTo(prev.x, prev.y);
      this.ctx.lineTo(curr.x, curr.y);
      this.ctx.stroke();
    }

    this.ctx.restore();
  }

  // Performance monitoring and adaptation
  monitorPerformance() {
    setInterval(() => {
      const fps = this.performanceMetrics.fps;

      if (fps < 30) {
        this.performanceMetrics.adaptiveLevel = 'low';
      } else if (fps < 45) {
        this.performanceMetrics.adaptiveLevel = 'medium';
      } else {
        this.performanceMetrics.adaptiveLevel = 'high';
      }
    }, 2000);
  }

  updatePerformanceMetrics() {
    const now = performance.now();
    const delta = now - this.performanceMetrics.lastTime;

    this.performanceMetrics.frameTime = delta;
    this.performanceMetrics.fps = 1000 / delta;
    this.performanceMetrics.lastTime = now;
  }

  adaptQuality() {
    const level = this.performanceMetrics.adaptiveLevel;

    switch (level) {
      case 'low':
        this.config.particleCount = 30;
        this.config.connectionDistance = 100;
        this.config.backgroundOpacity = 0.05;
        break;
      case 'medium':
        this.config.particleCount = 50;
        this.config.connectionDistance = 125;
        this.config.backgroundOpacity = 0.04;
        break;
      case 'high':
        this.config.particleCount = 80;
        this.config.connectionDistance = 150;
        this.config.backgroundOpacity = 0.03;
        break;
    }
  }

  getAdaptiveParticleCount() {
    const level = this.performanceMetrics.adaptiveLevel;

    switch (level) {
      case 'low': return 30;
      case 'medium': return 50;
      case 'high': return 80;
      default: return this.config.particleCount;
    }
  }

  // Public API methods
  addParticle(x, y, type = 'normal', color = null) {
    const particle = this.createParticle(x, y, type);
    if (color) particle.color = color;
    this.particles.push(particle);
  }

  addBurst(x, y, count = 10, color = null) {
    for (let i = 0; i < count; i++) {
      const angle = (i / count) * Math.PI * 2;
      const speed = 2 + Math.random() * 3;
      const particle = this.createParticle(x, y, 'temporary');
      particle.vx = Math.cos(angle) * speed;
      particle.vy = Math.sin(angle) * speed;
      if (color) particle.color = color;
      this.particles.push(particle);
    }
  }

  updateOptions(newOptions) {
    this.config = { ...this.config, ...newOptions };
  }

  getMetrics() {
    return {
      particleCount: this.particles.length,
      fps: Math.round(this.performanceMetrics.fps),
      adaptiveLevel: this.performanceMetrics.adaptiveLevel,
      isRunning: this.isRunning
    };
  }

  destroy() {
    this.pause();
    this.container.removeChild(this.canvas);
    this.particles = [];
  }
}

// Initialize particle system
document.addEventListener('DOMContentLoaded', () => {
  const heroParticles = document.getElementById('hero-particles');
  if (heroParticles) {
    window.heroParticleSystem = new AdvancedParticleSystem('hero-particles', {
      particleCount: 15,
      connectionDistance: 80,
      colors: ['rgba(0, 102, 204, 0.2)', 'rgba(44, 62, 80, 0.2)'],
      adaptiveQuality: true,
      glowIntensity: 0.05
    });
  }

  const showcaseParticles = document.getElementById('showcase-particles');
  if (showcaseParticles) {
    window.showcaseParticleSystem = new AdvancedParticleSystem('showcase-particles', {
      particleCount: 10,
      connectionDistance: 60,
      colors: ['rgba(0, 102, 204, 0.15)'],
      adaptiveQuality: true,
      glowIntensity: 0.05
    });
  }
});

// Make available globally for non-module usage
window.AdvancedParticleSystem = AdvancedParticleSystem;