(function () {
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.addEventListener('DOMContentLoaded', () => {
    initMetricCounters();
    initFeatureCarousel();
    initPlatformToggle();
    initFaqAccordions();
    initCtaPulse();
    initParticles();
  });

  function initMetricCounters() {
    const counters = document.querySelectorAll('.metric');
    if (!counters.length || prefersReducedMotion) return;

    const observer = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.35 }
    );

    counters.forEach((counter) => observer.observe(counter));
  }

  function animateCounter(el) {
    const valueEl = el.querySelector('.metric__value');
    const target = Number(el.dataset.target || 0);
    const duration = 1800;
    const start = performance.now();

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = easeOutCubic(progress);
      const value = Math.floor(target * eased);
      valueEl.textContent = value;
      if (progress < 1) {
        requestAnimationFrame(tick);
      } else {
        valueEl.textContent = target;
      }
    }

    requestAnimationFrame(tick);
  }

  function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  function initFeatureCarousel() {
    const track = document.querySelector('.feature-carousel__track');
    const dots = Array.from(document.querySelectorAll('.feature-carousel__dot'));
    if (!track || !dots.length) return;

    const cards = Array.from(track.querySelectorAll('.feature-card'));
    let activeIndex = 0;

    const updateActiveDot = (index) => {
      if (index === activeIndex) return;
      dots[activeIndex]?.classList.remove('is-active');
      dots[index]?.classList.add('is-active');
      dots[activeIndex]?.setAttribute('aria-selected', 'false');
      dots[index]?.setAttribute('aria-selected', 'true');
      activeIndex = index;
    };

    dots.forEach((dot, idx) => {
      dot.addEventListener('click', () => {
        cards[idx]?.scrollIntoView({ behavior: prefersReducedMotion ? 'auto' : 'smooth', inline: 'center', block: 'nearest' });
        updateActiveDot(idx);
      });
      dot.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          cards[idx]?.scrollIntoView({ behavior: prefersReducedMotion ? 'auto' : 'smooth', inline: 'center', block: 'nearest' });
          updateActiveDot(idx);
        }
      });
    });

    let debounceTimer = null;
    track.addEventListener('scroll', () => {
      if (debounceTimer) cancelAnimationFrame(debounceTimer);
      debounceTimer = requestAnimationFrame(() => {
        const scrollLeft = track.scrollLeft;
        const cardWidth = cards[0]?.offsetWidth || 1;
        const gap = parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap || 0);
        const index = Math.round(scrollLeft / (cardWidth + gap));
        if (index >= 0 && index < cards.length) {
          updateActiveDot(index);
        }
      });
    });
  }

  function initPlatformToggle() {
    const chips = Array.from(document.querySelectorAll('.cta__chip'));
    const button = document.getElementById('downloadCta');
    if (!chips.length || !button) return;

    const labels = {
      mac: 'macOS',
      windows: 'Windows',
      linux: 'Linux'
    };

    chips.forEach((chip) => {
      chip.addEventListener('click', () => handlePlatformChange(chip));
      chip.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          handlePlatformChange(chip);
        }
      });
    });

    function handlePlatformChange(activeChip) {
      const selected = activeChip.dataset.platform;
      chips.forEach((chip) => {
        const isSelected = chip === activeChip;
        chip.classList.toggle('is-selected', isSelected);
        chip.setAttribute('aria-checked', String(isSelected));
      });
      const label = labels[selected] || 'macOS';
      button.textContent = `Download for ${label}`;
      button.dataset.platformLabel = label;
      button.dataset.platform = selected;
    }
  }

  function initFaqAccordions() {
    const questions = document.querySelectorAll('.faq__question');
    if (!questions.length) return;

    questions.forEach((question) => {
      const answer = question.nextElementSibling;
      if (!answer) return;
      question.addEventListener('click', () => toggleAnswer(question, answer));
      question.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          toggleAnswer(question, answer);
        }
      });
    });
  }

  function toggleAnswer(question, answer) {
    const isExpanded = question.getAttribute('aria-expanded') === 'true';
    question.setAttribute('aria-expanded', String(!isExpanded));
    if (!isExpanded) {
      answer.hidden = false;
      answer.classList.add('is-open');
      const contentHeight = answer.scrollHeight;
      answer.style.maxHeight = contentHeight + 'px';
      const onOpenEnd = (event) => {
        if (event.propertyName === 'max-height') {
          answer.style.maxHeight = 'none';
          answer.removeEventListener('transitionend', onOpenEnd);
        }
      };
      answer.addEventListener('transitionend', onOpenEnd);
    } else {
      const currentHeight = answer.scrollHeight;
      answer.style.maxHeight = currentHeight + 'px';
      requestAnimationFrame(() => {
        answer.style.maxHeight = '0px';
        answer.classList.remove('is-open');
      });
      const onCloseEnd = (event) => {
        if (event.propertyName === 'max-height') {
          answer.hidden = true;
          answer.style.maxHeight = null;
          answer.removeEventListener('transitionend', onCloseEnd);
        }
      };
      answer.addEventListener('transitionend', onCloseEnd);
    }
  }

  function initCtaPulse() {
    const button = document.getElementById('downloadCta');
    if (!button || prefersReducedMotion) return;
    setInterval(() => {
      button.classList.add('cta--pulse');
      window.setTimeout(() => button.classList.remove('cta--pulse'), 1200);
    }, 12000);
  }

  function initParticles() {
    const field = document.getElementById('particle-field');
    if (!field || prefersReducedMotion) return;
    const total = 28;
    for (let i = 0; i < total; i += 1) {
      const particle = document.createElement('span');
      particle.className = 'hero__particle';
      const size = Math.random() * 4 + 3;
      particle.style.width = `${size}px`;
      particle.style.height = `${size}px`;
      particle.style.left = `${Math.random() * 100}%`;
      particle.style.bottom = `${Math.random() * 60}%`;
      const duration = 12 + Math.random() * 12;
      const delay = Math.random() * -20;
      particle.style.animationDuration = `${duration}s`;
      particle.style.animationDelay = `${delay}s`;
      field.appendChild(particle);
    }
  }
})();
