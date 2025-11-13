// 3D Signature Canvas Animation
const sig3dCanvas = document.getElementById('signature-3d');
const sig3dCtx = sig3dCanvas.getContext('2d');

let angle = 0;

function drawSignature3D() {
  sig3dCtx.clearRect(0, 0, sig3dCanvas.width, sig3dCanvas.height);
  
  sig3dCtx.save();
  sig3dCtx.translate(sig3dCanvas.width / 2, sig3dCanvas.height / 2);
  sig3dCtx.rotate(angle);
  
  const gradient = sig3dCtx.createLinearGradient(-150, 0, 150, 0);
  gradient.addColorStop(0, '#f4a261');
  gradient.addColorStop(1, '#52b788');
  
  sig3dCtx.strokeStyle = gradient;
  sig3dCtx.lineWidth = 8;
  sig3dCtx.lineCap = 'round';
  sig3dCtx.lineJoin = 'round';
  
  sig3dCtx.beginPath();
  sig3dCtx.moveTo(-150, 0);
  sig3dCtx.quadraticCurveTo(-100, -50, -50, 0);
  sig3dCtx.quadraticCurveTo(0, 50, 50, 0);
  sig3dCtx.quadraticCurveTo(100, -30, 150, 0);
  sig3dCtx.stroke();
  
  sig3dCtx.restore();
  
  angle += 0.005;
  requestAnimationFrame(drawSignature3D);
}

drawSignature3D();

// Scroll Animations
const scrollObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, {
  threshold: 0.1,
  rootMargin: '0px 0px -100px 0px'
});

document.querySelectorAll('.glass-card, .bento-item').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(30px)';
  el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
  scrollObserver.observe(el);
});

const style = document.createElement('style');
style.textContent = `
  .visible {
    opacity: 1 !important;
    transform: translateY(0) !important;
  }
`;
document.head.appendChild(style);
