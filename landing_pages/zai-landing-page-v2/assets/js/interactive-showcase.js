/**
 * Signature Extractor - Interactive Showcase
 * Advanced signature extraction visualization with real-time interaction
 */

class InteractiveShowcase {
  constructor() {
    this.canvas = document.getElementById('signature-canvas');
    this.ctx = this.canvas.getContext('2d');
    this.isProcessing = false;
    this.currentStep = 0;
    this.particles = [];
    this.signaturePoints = [];
    this.isDrawing = false;
    this.mousePos = { x: 0, y: 0 };
    this.detectionZones = [];
    this.extractionProgress = 0;
    this.qualityScore = 0;

    // Configuration
    this.config = {
      particleCount: 50,
      detectionZoneCount: 3,
      extractionDuration: 3000,
      qualityAnalysisDuration: 2000,
      particleColors: ['#00ff88', '#00d4ff', '#7b2ff7', '#ff6b6b'],
      glowIntensity: 0.8,
      lineSmoothness: 0.4,
      detectionPulseSpeed: 0.002
    };

    this.init();
  }

  init() {
    this.setupCanvas();
    this.createDetectionZones();
    this.initializeParticles();
    this.bindEvents();
    this.startIdleAnimation();
  }

  setupCanvas() {
    const rect = this.canvas.getBoundingClientRect();
    this.canvas.width = rect.width * window.devicePixelRatio;
    this.canvas.height = rect.height * window.devicePixelRatio;
    this.ctx.scale(window.devicePixelRatio, window.devicePixelRatio);

    // Set canvas styles
    this.canvas.style.filter = 'drop-shadow(0 0 30px rgba(0, 255, 136, 0.3))';
  }

  createDetectionZones() {
    const zoneCount = this.config.detectionZoneCount;
    const centerX = this.canvas.width / (2 * window.devicePixelRatio);
    const centerY = this.canvas.height / (2 * window.devicePixelRatio);
    const radius = Math.min(centerX, centerY) * 0.6;

    for (let i = 0; i < zoneCount; i++) {
      const angle = (i / zoneCount) * Math.PI * 2;
      const zoneRadius = radius * (0.3 + Math.random() * 0.4);

      this.detectionZones.push({
        x: centerX + Math.cos(angle) * zoneRadius,
        y: centerY + Math.sin(angle) * zoneRadius,
        radius: 30 + Math.random() * 20,
        active: false,
        detected: false,
        confidence: 0,
        pulsePhase: Math.random() * Math.PI * 2,
        color: this.config.particleColors[i % this.config.particleColors.length]
      });
    }
  }

  initializeParticles() {
    for (let i = 0; i < this.config.particleCount; i++) {
      this.particles.push(this.createParticle());
    }
  }

  createParticle() {
    const rect = this.canvas.getBoundingClientRect();
    return {
      x: Math.random() * rect.width,
      y: Math.random() * rect.height,
      vx: (Math.random() - 0.5) * 0.5,
      vy: (Math.random() - 0.5) * 0.5,
      radius: Math.random() * 2 + 1,
      color: this.config.particleColors[Math.floor(Math.random() * this.config.particleColors.length)],
      alpha: Math.random() * 0.5 + 0.5,
      life: 1,
      maxLife: Math.random() * 100 + 100,
      type: Math.random() > 0.5 ? 'float' : 'orbit',
      orbitCenter: {
        x: this.canvas.width / (2 * window.devicePixelRatio),
        y: this.canvas.height / (2 * window.devicePixelRatio)
      },
      orbitRadius: Math.random() * 100 + 50,
      orbitAngle: Math.random() * Math.PI * 2,
      orbitSpeed: (Math.random() - 0.5) * 0.02
    };
  }

  bindEvents() {
    // Mouse interactions
    this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
    this.canvas.addEventListener('mousedown', (e) => this.handleMouseDown(e));
    this.canvas.addEventListener('mouseup', () => this.handleMouseUp());
    this.canvas.addEventListener('mouseleave', () => this.handleMouseLeave());

    // Touch interactions
    this.canvas.addEventListener('touchstart', (e) => this.handleTouchStart(e));
    this.canvas.addEventListener('touchmove', (e) => this.handleTouchMove(e));
    this.canvas.addEventListener('touchend', () => this.handleTouchEnd());

    // Button interactions
    const startBtn = document.getElementById('start-extraction');
    const resetBtn = document.getElementById('reset-canvas');

    if (startBtn) {
      startBtn.addEventListener('click', () => this.startExtraction());
    }

    if (resetBtn) {
      resetBtn.addEventListener('click', () => this.resetCanvas());
    }

    // Window resize
    window.addEventListener('resize', () => this.handleResize());
  }

  handleMouseMove(e) {
    const rect = this.canvas.getBoundingClientRect();
    this.mousePos = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    };

    if (this.isDrawing && !this.isProcessing) {
      this.addSignaturePoint(this.mousePos.x, this.mousePos.y);
    }
  }

  handleMouseDown(e) {
    if (!this.isProcessing) {
      this.isDrawing = true;
      this.signaturePoints = [];
      const rect = this.canvas.getBoundingClientRect();
      this.addSignaturePoint(e.clientX - rect.left, e.clientY - rect.top);
    }
  }

  handleMouseUp() {
    this.isDrawing = false;
    if (this.signaturePoints.length > 10 && !this.isProcessing) {
      this.analyzeSignature();
    }
  }

  handleMouseLeave() {
    this.isDrawing = false;
  }

  handleTouchStart(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const rect = this.canvas.getBoundingClientRect();
    const mouseEvent = new MouseEvent('mousedown', {
      clientX: touch.clientX,
      clientY: touch.clientY
    });
    this.handleMouseDown(mouseEvent);
  }

  handleTouchMove(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const rect = this.canvas.getBoundingClientRect();
    const mouseEvent = new MouseEvent('mousemove', {
      clientX: touch.clientX,
      clientY: touch.clientY
    });
    this.handleMouseMove(mouseEvent);
  }

  handleTouchEnd(e) {
    e.preventDefault();
    this.handleMouseUp();
  }

  handleResize() {
    this.setupCanvas();
  }

  addSignaturePoint(x, y) {
    this.signaturePoints.push({
      x, y,
      pressure: 0.8 + Math.random() * 0.2,
      timestamp: Date.now(),
      velocity: 0
    });

    // Calculate velocity for smoothing
    if (this.signaturePoints.length > 1) {
      const prev = this.signaturePoints[this.signaturePoints.length - 2];
      const curr = this.signaturePoints[this.signaturePoints.length - 1];
      const dx = curr.x - prev.x;
      const dy = curr.y - prev.y;
      const dt = curr.timestamp - prev.timestamp;
      curr.velocity = Math.sqrt(dx * dx + dy * dy) / dt;
    }

    // Limit points for performance
    if (this.signaturePoints.length > 500) {
      this.signaturePoints.shift();
    }
  }

  startExtraction() {
    if (this.isProcessing) return;

    this.isProcessing = true;
    this.currentStep = 1;
    this.extractionProgress = 0;

    // Create a sample signature if none exists
    if (this.signaturePoints.length < 20) {
      this.createSampleSignature();
    }

    this.runExtractionProcess();
  }

  createSampleSignature() {
    const rect = this.canvas.getBoundingClientRect();
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    // Generate a realistic signature path
    this.signaturePoints = [];
    const points = [
      { x: centerX - 60, y: centerY },
      { x: centerX - 40, y: centerY - 20 },
      { x: centerX - 20, y: centerY + 10 },
      { x: centerX, y: centerY - 15 },
      { x: centerX + 20, y: centerY + 20 },
      { x: centerX + 40, y: centerY },
      { x: centerX + 60, y: centerY - 25 }
    ];

    for (let i = 0; i < points.length; i++) {
      const point = points[i];
      // Add some randomness for natural look
      this.signaturePoints.push({
        x: point.x + (Math.random() - 0.5) * 10,
        y: point.y + (Math.random() - 0.5) * 10,
        pressure: 0.7 + Math.random() * 0.3,
        timestamp: Date.now() + i * 50,
        velocity: 2 + Math.random() * 3
      });
    }
  }

  async runExtractionProcess() {
    const steps = [
      { name: 'Scanning', duration: 1000, action: () => this.scanForSignatures() },
      { name: 'Detection', duration: 1500, action: () => this.detectSignatureRegions() },
      { name: 'Analysis', duration: 1200, action: () => this.analyzeSignatureQuality() },
      { name: 'Extraction', duration: 800, action: () => this.extractSignature() },
      { name: 'Optimization', duration: 1000, action: () => this.optimizeSignature() }
    ];

    for (let i = 0; i < steps.length; i++) {
      const step = steps[i];
      this.updateUIStep(i + 1, step.name);

      await new Promise(resolve => {
        step.action();
        setTimeout(resolve, step.duration);
      });

      this.currentStep = i + 2;
    }

    this.completeExtraction();
  }

  scanForSignatures() {
    // Activate all detection zones with scanning animation
    this.detectionZones.forEach((zone, index) => {
      setTimeout(() => {
        zone.active = true;
        zone.detected = false;
        zone.confidence = 0;
      }, index * 100);
    });
  }

  detectSignatureRegions() {
    // Simulate signature detection in zones
    this.detectionZones.forEach((zone, index) => {
      setTimeout(() => {
        if (Math.random() > 0.3) { // 70% detection rate
          zone.detected = true;
          zone.confidence = 0.7 + Math.random() * 0.3;
          this.createDetectionParticles(zone);
        }
      }, 500 + index * 200);
    });
  }

  analyzeSignatureQuality() {
    // Simulate quality analysis
    const analysisFactors = ['clarity', 'contrast', 'completeness', 'noise'];
    let totalScore = 0;

    analysisFactors.forEach((factor, index) => {
      setTimeout(() => {
        const factorScore = 0.6 + Math.random() * 0.4;
        totalScore += factorScore;
        this.updateQualityFactor(factor, factorScore);
      }, index * 300);
    });

    setTimeout(() => {
      this.qualityScore = Math.min(95, (totalScore / analysisFactors.length) * 100);
      this.updateQualityScore(this.qualityScore);
    }, analysisFactors.length * 300);
  }

  extractSignature() {
    // Create extraction effect
    this.createExtractionEffect();
    this.extractionProgress = 0;

    const extractionInterval = setInterval(() => {
      this.extractionProgress += 5;
      this.updateExtractionProgress(this.extractionProgress);

      if (this.extractionProgress >= 100) {
        clearInterval(extractionInterval);
      }
    }, 50);
  }

  optimizeSignature() {
    // Create optimization effect
    this.createOptimizationEffect();
  }

  createDetectionParticles(zone) {
    for (let i = 0; i < 10; i++) {
      const particle = {
        x: zone.x,
        y: zone.y,
        vx: (Math.random() - 0.5) * 4,
        vy: (Math.random() - 0.5) * 4,
        radius: Math.random() * 3 + 1,
        color: zone.color,
        alpha: 1,
        life: 1,
        maxLife: 60,
        type: 'detection',
        decay: 0.02
      };
      this.particles.push(particle);
    }
  }

  createExtractionEffect() {
    const rect = this.canvas.getBoundingClientRect();
    for (let i = 0; i < 30; i++) {
      const angle = (i / 30) * Math.PI * 2;
      const particle = {
        x: rect.width / 2,
        y: rect.height / 2,
        vx: Math.cos(angle) * 3,
        vy: Math.sin(angle) * 3,
        radius: Math.random() * 4 + 2,
        color: this.config.particleColors[Math.floor(Math.random() * this.config.particleColors.length)],
        alpha: 1,
        life: 1,
        maxLife: 80,
        type: 'extraction',
        decay: 0.015
      };
      this.particles.push(particle);
    }
  }

  createOptimizationEffect() {
    this.signaturePoints.forEach((point, index) => {
      setTimeout(() => {
        const particle = {
          x: point.x,
          y: point.y,
          vx: (Math.random() - 0.5) * 2,
          vy: -Math.random() * 2 - 1,
          radius: Math.random() * 2 + 1,
          color: '#00ff88',
          alpha: 0.8,
          life: 1,
          maxLife: 40,
          type: 'optimization',
          decay: 0.025
        };
        this.particles.push(particle);
      }, index * 2);
    });
  }

  completeExtraction() {
    this.isProcessing = false;
    this.currentStep = 6;
    this.updateUIStep(6, 'Complete');
    this.showResults();
  }

  resetCanvas() {
    this.isProcessing = false;
    this.currentStep = 0;
    this.signaturePoints = [];
    this.extractionProgress = 0;
    this.qualityScore = 0;

    // Reset detection zones
    this.detectionZones.forEach(zone => {
      zone.active = false;
      zone.detected = false;
      zone.confidence = 0;
    });

    // Reset UI
    this.updateUIStep(0, 'Ready');
    this.updateExtractionProgress(0);
    this.updateQualityScore(0);

    // Hide results
    this.hideResults();
  }

  updateUIStep(step, name) {
    const stepElement = document.getElementById('current-step');
    const stepNameElement = document.getElementById('step-name');

    if (stepElement) stepElement.textContent = step;
    if (stepNameElement) stepNameElement.textContent = name;

    // Update step indicators
    document.querySelectorAll('.step-indicator').forEach((indicator, index) => {
      indicator.classList.toggle('active', index < step);
      indicator.classList.toggle('current', index === step - 1);
    });
  }

  updateExtractionProgress(progress) {
    const progressBar = document.getElementById('extraction-progress');
    const progressText = document.getElementById('progress-text');

    if (progressBar) {
      progressBar.style.width = `${progress}%`;
      progressBar.style.background = `linear-gradient(90deg, #00ff88 0%, #00d4ff ${progress}%, rgba(255,255,255,0.1) ${progress}%)`;
    }

    if (progressText) progressText.textContent = `${Math.round(progress)}%`;
  }

  updateQualityScore(score) {
    const scoreElement = document.getElementById('quality-score');
    const scoreRing = document.getElementById('score-ring');

    if (scoreElement) scoreElement.textContent = `${Math.round(score)}%`;

    if (scoreRing) {
      const circumference = 2 * Math.PI * 45;
      const offset = circumference - (score / 100) * circumference;
      scoreRing.style.strokeDashoffset = offset;
    }
  }

  updateQualityFactor(factor, score) {
    const factorElement = document.getElementById(`factor-${factor}`);
    if (factorElement) {
      factorElement.style.width = `${score * 100}%`;
      factorElement.style.background = score > 0.8 ? '#00ff88' : score > 0.6 ? '#00d4ff' : '#ff6b6b';
    }
  }

  showResults() {
    const resultsElement = document.getElementById('extraction-results');
    if (resultsElement) {
      resultsElement.classList.add('show');
    }
  }

  hideResults() {
    const resultsElement = document.getElementById('extraction-results');
    if (resultsElement) {
      resultsElement.classList.remove('show');
    }
  }

  startIdleAnimation() {
    this.animate();
  }

  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Update and draw particles
    this.updateParticles();
    this.drawParticles();

    // Update and draw detection zones
    this.updateDetectionZones();
    this.drawDetectionZones();

    // Draw signature
    if (this.signaturePoints.length > 0) {
      this.drawSignature();
    }

    // Draw connections
    this.drawConnections();

    requestAnimationFrame(() => this.animate());
  }

  updateParticles() {
    this.particles = this.particles.filter(particle => {
      particle.life -= 1 / particle.maxLife;

      if (particle.life <= 0) return false;

      switch (particle.type) {
        case 'float':
          particle.x += particle.vx;
          particle.y += particle.vy;
          break;

        case 'orbit':
          particle.orbitAngle += particle.orbitSpeed;
          particle.x = particle.orbitCenter.x + Math.cos(particle.orbitAngle) * particle.orbitRadius;
          particle.y = particle.orbitCenter.y + Math.sin(particle.orbitAngle) * particle.orbitRadius;
          break;

        case 'detection':
        case 'extraction':
        case 'optimization':
          particle.x += particle.vx;
          particle.y += particle.vy;
          particle.vx *= 0.98;
          particle.vy *= 0.98;
          if (particle.decay) {
            particle.life -= particle.decay;
          }
          break;
      }

      // Mouse interaction
      const dx = particle.x - this.mousePos.x;
      const dy = particle.y - this.mousePos.y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < 100) {
        const force = (100 - distance) / 100;
        particle.x += dx * force * 0.02;
        particle.y += dy * force * 0.02;
      }

      // Boundary check
      const rect = this.canvas.getBoundingClientRect();
      if (particle.x < 0 || particle.x > rect.width ||
          particle.y < 0 || particle.y > rect.height) {
        if (particle.type === 'float' || particle.type === 'orbit') {
          // Reset particle to center
          particle.x = rect.width / 2;
          particle.y = rect.height / 2;
        }
      }

      return true;
    });

    // Maintain particle count
    while (this.particles.length < this.config.particleCount) {
      this.particles.push(this.createParticle());
    }
  }

  updateDetectionZones() {
    this.detectionZones.forEach(zone => {
      if (zone.active) {
        zone.pulsePhase += this.config.detectionPulseSpeed * Math.PI * 2;

        if (zone.detected) {
          // Pulsing effect when detected
          zone.radius = 30 + Math.sin(zone.pulsePhase) * 5;
        }
      }
    });
  }

  drawParticles() {
    this.particles.forEach(particle => {
      this.ctx.save();

      this.ctx.globalAlpha = particle.alpha * particle.life;
      this.ctx.fillStyle = particle.color;
      this.ctx.shadowBlur = 10;
      this.ctx.shadowColor = particle.color;

      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      this.ctx.fill();

      this.ctx.restore();
    });
  }

  drawDetectionZones() {
    this.detectionZones.forEach(zone => {
      if (!zone.active) return;

      this.ctx.save();

      // Draw detection zone
      this.ctx.strokeStyle = zone.detected ? zone.color : 'rgba(255, 255, 255, 0.3)';
      this.ctx.lineWidth = zone.detected ? 2 : 1;
      this.ctx.setLineDash(zone.detected ? [] : [5, 5]);

      if (zone.detected) {
        this.ctx.shadowBlur = 20;
        this.ctx.shadowColor = zone.color;
      }

      this.ctx.beginPath();
      this.ctx.arc(zone.x, zone.y, zone.radius, 0, Math.PI * 2);
      this.ctx.stroke();

      // Draw confidence indicator
      if (zone.detected && zone.confidence > 0) {
        this.ctx.fillStyle = zone.color;
        this.ctx.font = '12px monospace';
        this.ctx.fillText(`${Math.round(zone.confidence * 100)}%`, zone.x - 15, zone.y - zone.radius - 5);
      }

      this.ctx.restore();
    });
  }

  drawSignature() {
    if (this.signaturePoints.length < 2) return;

    this.ctx.save();
    this.ctx.lineCap = 'round';
    this.ctx.lineJoin = 'round';

    for (let i = 1; i < this.signaturePoints.length; i++) {
      const prev = this.signaturePoints[i - 1];
      const curr = this.signaturePoints[i];

      // Smooth line using quadratic curve
      const cpx = (prev.x + curr.x) / 2;
      const cpy = (prev.y + curr.y) / 2;

      this.ctx.strokeStyle = this.isProcessing ? '#00ff88' : '#ffffff';
      this.ctx.lineWidth = (prev.pressure + curr.pressure) * 2;
      this.ctx.globalAlpha = this.isProcessing ? 0.8 : 0.9;

      this.ctx.shadowBlur = 10;
      this.ctx.shadowColor = this.isProcessing ? '#00ff88' : '#ffffff';

      this.ctx.beginPath();
      this.ctx.moveTo(prev.x, prev.y);
      this.ctx.quadraticCurveTo(prev.x, prev.y, cpx, cpy);
      this.ctx.stroke();
    }

    this.ctx.restore();
  }

  drawConnections() {
    // Draw connections between nearby particles
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const p1 = this.particles[i];
        const p2 = this.particles[j];

        const dx = p1.x - p2.x;
        const dy = p1.y - p2.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 80) {
          this.ctx.save();
          this.ctx.globalAlpha = (80 - distance) / 80 * 0.2 * p1.life * p2.life;
          this.ctx.strokeStyle = '#00ff88';
          this.ctx.lineWidth = 0.5;

          this.ctx.beginPath();
          this.ctx.moveTo(p1.x, p1.y);
          this.ctx.lineTo(p2.x, p2.y);
          this.ctx.stroke();

          this.ctx.restore();
        }
      }
    }
  }

  analyzeSignature() {
    // Basic signature analysis
    if (this.signaturePoints.length > 10) {
      this.startExtraction();
    }
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('signature-canvas');
  if (canvas) {
    window.interactiveShowcase = new InteractiveShowcase();
  }
});

// Make available globally for non-module usage
window.InteractiveShowcase = InteractiveShowcase;