// ============================================
// Advanced Animations for Signature Extractor Landing Page
// ============================================

// ============================================
// Parallax Effect
// ============================================
function initParallax() {
    const hero = document.querySelector('.hero');
    if (!hero) return;

    const blobs = document.querySelectorAll('.blob');
    const meshGradient = document.querySelector('.mesh-gradient');

    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const heroHeight = hero.offsetHeight;

        // Only apply parallax within hero section
        if (scrolled < heroHeight) {
            // Move blobs at different speeds
            blobs.forEach((blob, index) => {
                const speed = 0.3 + (index * 0.1);
                const yPos = scrolled * speed;
                blob.style.transform = `translateY(${yPos}px)`;
            });

            // Subtle mesh gradient movement
            if (meshGradient) {
                meshGradient.style.transform = `translateY(${scrolled * 0.2}px)`;
            }
        }
    });
}

// ============================================
// Stagger Animation
// ============================================
function initStaggerAnimations() {
    const staggerContainers = document.querySelectorAll('.hero-features, .problem-grid, .social-proof-content');

    staggerContainers.forEach(container => {
        const children = container.children;
        Array.from(children).forEach((child, index) => {
            child.style.animationDelay = `${index * 0.1}s`;
            child.classList.add('animate-fade-up');
        });
    });
}

// ============================================
// Number Counter Animation
// ============================================
function animateCounters() {
    const counters = document.querySelectorAll('.proof-number');

    counters.forEach(counter => {
        const target = counter.textContent;
        const isNumber = /^\d+$/.test(target.replace(/,/g, ''));

        if (!isNumber) return;

        const finalValue = parseInt(target.replace(/,/g, ''));
        let current = 0;
        const increment = finalValue / 50; // 50 steps
        const duration = 2000; // 2 seconds
        const stepTime = duration / 50;

        counter.textContent = '0';

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const timer = setInterval(() => {
                        current += increment;
                        if (current >= finalValue) {
                            counter.textContent = formatNumber(finalValue);
                            clearInterval(timer);
                        } else {
                            counter.textContent = formatNumber(Math.floor(current));
                        }
                    }, stepTime);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        observer.observe(counter);
    });
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// ============================================
// Typing Animation
// ============================================
function createTypingEffect(element, text, speed = 50) {
    let index = 0;
    element.textContent = '';

    function type() {
        if (index < text.length) {
            element.textContent += text.charAt(index);
            index++;
            setTimeout(type, speed);
        }
    }

    type();
}

// ============================================
// Card Tilt Effect (3D)
// ============================================
function initCardTilt() {
    const cards = document.querySelectorAll('.problem-card, .pricing-card');

    cards.forEach(card => {
        card.addEventListener('mousemove', handleTilt);
        card.addEventListener('mouseleave', handleTiltReset);
    });
}

function handleTilt(e) {
    const card = e.currentTarget;
    const rect = card.getBoundingClientRect();

    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotateX = (y - centerY) / 20;
    const rotateY = (centerX - x) / 20;

    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
    card.style.transition = 'transform 0.1s ease';
}

function handleTiltReset(e) {
    const card = e.currentTarget;
    card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
    card.style.transition = 'transform 0.5s ease';
}

// ============================================
// Smooth Scroll with Easing
// ============================================
function smoothScrollTo(target, duration = 1000) {
    const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - 72;
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;
    let startTime = null;

    function animation(currentTime) {
        if (startTime === null) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const run = easeInOutCubic(timeElapsed, startPosition, distance, duration);
        window.scrollTo(0, run);
        if (timeElapsed < duration) requestAnimationFrame(animation);
    }

    function easeInOutCubic(t, b, c, d) {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t * t + b;
        t -= 2;
        return c / 2 * (t * t * t + 2) + b;
    }

    requestAnimationFrame(animation);
}

// ============================================
// Magnetic Button Effect
// ============================================
function initMagneticButtons() {
    const buttons = document.querySelectorAll('.btn-primary');

    buttons.forEach(button => {
        button.addEventListener('mousemove', (e) => {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;

            button.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
        });

        button.addEventListener('mouseleave', () => {
            button.style.transform = 'translate(0, 0)';
        });
    });
}

// ============================================
// Gradient Animation
// ============================================
function initGradientAnimation() {
    const gradientTexts = document.querySelectorAll('.gradient-text');

    gradientTexts.forEach(text => {
        let hue = 200;

        setInterval(() => {
            hue = (hue + 1) % 360;
            const color1 = `hsl(${hue}, 80%, 60%)`;
            const color2 = `hsl(${(hue + 60) % 360}, 80%, 60%)`;

            text.style.backgroundImage = `linear-gradient(135deg, ${color1} 0%, ${color2} 100%)`;
        }, 50);
    });
}

// ============================================
// Text Reveal Animation
// ============================================
function initTextReveal() {
    const titles = document.querySelectorAll('.section-title');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const text = entry.target.textContent;
                entry.target.textContent = '';
                entry.target.style.opacity = '1';

                let index = 0;
                const interval = setInterval(() => {
                    if (index < text.length) {
                        entry.target.textContent += text[index];
                        index++;
                    } else {
                        clearInterval(interval);
                    }
                }, 30);

                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    titles.forEach(title => {
        observer.observe(title);
    });
}

// ============================================
// Cursor Trail Effect
// ============================================
function initCursorTrail() {
    const hero = document.querySelector('.hero');
    if (!hero) return;

    const trail = [];
    const trailLength = 10;

    hero.addEventListener('mousemove', (e) => {
        const dot = document.createElement('div');
        dot.className = 'cursor-trail';
        dot.style.left = e.clientX + 'px';
        dot.style.top = e.clientY + 'px';

        document.body.appendChild(dot);

        trail.push(dot);

        if (trail.length > trailLength) {
            const oldDot = trail.shift();
            oldDot.remove();
        }

        setTimeout(() => {
            dot.style.opacity = '0';
            dot.style.transform = 'scale(0)';
            setTimeout(() => dot.remove(), 300);
        }, 300);
    });

    // Add styles for cursor trail
    const style = document.createElement('style');
    style.innerHTML = `
        .cursor-trail {
            position: fixed;
            width: 8px;
            height: 8px;
            background: rgba(59, 130, 246, 0.5);
            border-radius: 50%;
            pointer-events: none;
            transform: translate(-50%, -50%) scale(1);
            transition: opacity 0.3s, transform 0.3s;
            z-index: 9999;
        }
    `;
    document.head.appendChild(style);
}

// ============================================
// Background Music Visualizer (Optional)
// ============================================
function initVisualizer() {
    const canvas = document.createElement('canvas');
    canvas.id = 'visualizer';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.opacity = '0.1';
    canvas.style.zIndex = '-1';

    document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];
    const particleCount = 50;

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 2 + 1,
            dx: (Math.random() - 0.5) * 0.5,
            dy: (Math.random() - 0.5) * 0.5,
            color: `hsla(${Math.random() * 60 + 200}, 80%, 60%, 0.5)`
        });
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach(particle => {
            particle.x += particle.dx;
            particle.y += particle.dy;

            if (particle.x < 0 || particle.x > canvas.width) particle.dx *= -1;
            if (particle.y < 0 || particle.y > canvas.height) particle.dy *= -1;

            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            ctx.fillStyle = particle.color;
            ctx.fill();
        });

        requestAnimationFrame(animate);
    }

    animate();
}

// ============================================
// Initialize All Animations
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    // Basic animations
    initParallax();
    initStaggerAnimations();
    animateCounters();

    // Advanced interactions
    initCardTilt();
    initMagneticButtons();

    // Optional effects (can be toggled)
    // initGradientAnimation();
    // initTextReveal();
    // initCursorTrail();
    // initVisualizer();
});

// ============================================
// Performance Monitoring
// ============================================
if (window.performance) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = window.performance.timing;
            const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
            console.log(`Page load time: ${pageLoadTime}ms`);
        }, 0);
    });
}

// ============================================
// Smooth Scrolling Polyfill
// ============================================
if (!('scrollBehavior' in document.documentElement.style)) {
    const originalScrollTo = window.scrollTo;
    window.scrollTo = function(x, y) {
        if (typeof x === 'object') {
            if (x.behavior === 'smooth') {
                smoothScrollTo({ getBoundingClientRect: () => ({ top: x.top || 0 }) });
                return;
            }
        }
        originalScrollTo.call(window, x, y);
    };
}
