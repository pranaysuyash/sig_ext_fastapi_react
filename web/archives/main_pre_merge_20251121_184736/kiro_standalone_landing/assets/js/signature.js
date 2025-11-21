const canvas = document.getElementById('signature-canvas');
const ctx = canvas.getContext('2d');

let angle = 0;
let scale = 1;
let direction = 1;

function drawSignature() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  ctx.save();
  ctx.translate(canvas.width / 2, canvas.height / 2);
  ctx.rotate(angle);
  ctx.scale(scale, scale);
  
  const gradient = ctx.createLinearGradient(-200, 0, 200, 0);
  gradient.addColorStop(0, '#f4a261');
  gradient.addColorStop(1, '#52b788');
  
  ctx.strokeStyle = gradient;
  ctx.lineWidth = 10;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  ctx.shadowColor = 'rgba(244, 162, 97, 0.5)';
  ctx.shadowBlur = 20;
  
  ctx.beginPath();
  ctx.moveTo(-200, 0);
  ctx.quadraticCurveTo(-150, -60, -100, 0);
  ctx.quadraticCurveTo(-50, 60, 0, 0);
  ctx.quadraticCurveTo(50, -40, 100, 0);
  ctx.quadraticCurveTo(150, 40, 200, 0);
  ctx.stroke();
  
  ctx.restore();
  
  angle += 0.003;
  scale += 0.001 * direction;
  
  if (scale > 1.1 || scale < 0.9) {
    direction *= -1;
  }
  
  requestAnimationFrame(drawSignature);
}

drawSignature();
