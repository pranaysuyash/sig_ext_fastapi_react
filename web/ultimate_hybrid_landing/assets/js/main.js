// Loading Screen
window.addEventListener('load', () => {
  setTimeout(() => {
    document.getElementById('loading-screen').classList.add('hidden');
  }, 2000);
});

// Navigation Scroll Behavior
let lastScroll = 0;
const nav = document.getElementById('nav');

window.addEventListener('scroll', () => {
  const currentScroll = window.pageYOffset;
  
  if (currentScroll > 100) {
    nav.classList.add('scrolled');
  } else {
    nav.classList.remove('scrolled');
  }
  
  if (currentScroll > lastScroll && currentScroll > 200) {
    nav.classList.add('hidden');
  } else {
    nav.classList.remove('hidden');
  }
  
  lastScroll = currentScroll;
});

// Animated Counters
const animateCounter = (element) => {
  const target = parseFloat(element.dataset.target);
  const duration = 2000;
  const start = 0;
  const increment = target / (duration / 16);
  let current = start;
  
  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      element.textContent = target % 1 === 0 ? target : target.toFixed(1);
      clearInterval(timer);
    } else {
      element.textContent = Math.floor(current);
    }
  }, 16);
};

const observerOptions = {
  threshold: 0.5,
  rootMargin: '0px'
};

const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
      animateCounter(entry.target);
      entry.target.classList.add('counted');
    }
  });
}, observerOptions);

document.querySelectorAll('.stat-number').forEach(counter => {
  counterObserver.observe(counter);
});

// Magnetic Buttons
document.querySelectorAll('.magnetic').forEach(button => {
  button.addEventListener('mousemove', (e) => {
    const rect = button.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    
    button.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
  });
  
  button.addEventListener('mouseleave', () => {
    button.style.transform = 'translate(0, 0)';
  });
});

// FAQ Accordion
document.querySelectorAll('.faq-question').forEach(question => {
  question.addEventListener('click', () => {
    const item = question.parentElement;
    const isActive = item.classList.contains('active');
    
    document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('active'));
    
    if (!isActive) {
      item.classList.add('active');
    }
  });
});

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// Mobile Menu Toggle
const menuToggle = document.getElementById('menu-toggle');
const navLinks = document.querySelector('.nav-links');

menuToggle?.addEventListener('click', () => {
  navLinks.classList.toggle('active');
  menuToggle.classList.toggle('active');
});
