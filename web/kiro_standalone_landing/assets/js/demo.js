const fileInput = document.getElementById('demo-file');
const demoCanvas = document.getElementById('demo-canvas');
const resultCanvas = document.getElementById('result-canvas');
const thresholdSlider = document.getElementById('threshold');
const colorPicker = document.getElementById('color-picker');
const extractBtn = document.getElementById('extract-btn');
const downloadBtn = document.getElementById('download-btn');

const demoCtx = demoCanvas?.getContext('2d');
const resultCtx = resultCanvas?.getContext('2d');

let currentImage = null;

if (fileInput) {
  fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const img = new Image();
        img.onload = () => {
          currentImage = img;
          const maxWidth = 400;
          const scale = Math.min(1, maxWidth / img.width);
          demoCanvas.width = img.width * scale;
          demoCanvas.height = img.height * scale;
          demoCtx.drawImage(img, 0, 0, demoCanvas.width, demoCanvas.height);
          extractBtn.disabled = false;
        };
        img.src = event.target.result;
      };
      reader.readAsDataURL(file);
    }
  });
  
  const uploadZone = document.querySelector('.upload-zone');
  if (uploadZone) {
    uploadZone.addEventListener('dragover', (e) => {
      e.preventDefault();
      uploadZone.style.borderColor = 'var(--color-warm-amber)';
    });
    
    uploadZone.addEventListener('dragleave', () => {
      uploadZone.style.borderColor = 'var(--color-warm-gray)';
    });
    
    uploadZone.addEventListener('drop', (e) => {
      e.preventDefault();
      uploadZone.style.borderColor = 'var(--color-warm-gray)';
      const file = e.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) {
        fileInput.files = e.dataTransfer.files;
        fileInput.dispatchEvent(new Event('change'));
      }
    });
  }
}

if (extractBtn) {
  extractBtn.disabled = true;
  extractBtn.addEventListener('click', () => {
    if (!currentImage) return;
    
    const threshold = parseInt(thresholdSlider.value);
    const colorToRemove = hexToRgb(colorPicker.value);
    
    const imageData = demoCtx.getImageData(0, 0, demoCanvas.width, demoCanvas.height);
    const data = imageData.data;
    
    for (let i = 0; i < data.length; i += 4) {
      const r = data[i];
      const g = data[i + 1];
      const b = data[i + 2];
      
      const colorDist = Math.sqrt(
        Math.pow(r - colorToRemove.r, 2) +
        Math.pow(g - colorToRemove.g, 2) +
        Math.pow(b - colorToRemove.b, 2)
      );
      
      if (colorDist < threshold) {
        data[i + 3] = 0;
      }
    }
    
    resultCanvas.width = demoCanvas.width;
    resultCanvas.height = demoCanvas.height;
    resultCtx.putImageData(imageData, 0, 0);
    downloadBtn.disabled = false;
  });
}

if (downloadBtn) {
  downloadBtn.disabled = true;
  downloadBtn.addEventListener('click', () => {
    if (!resultCanvas) return;
    const link = document.createElement('a');
    link.download = 'signature-extracted.png';
    link.href = resultCanvas.toDataURL('image/png');
    link.click();
  });
}

function hexToRgb(hex) {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : { r: 255, g: 255, b: 255 };
}
