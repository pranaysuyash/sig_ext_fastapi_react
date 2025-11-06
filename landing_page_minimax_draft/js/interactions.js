/* ============================================
   Interactive Elements
   Enhanced user interactions and micro-animations
   ============================================ */

// Interactive Elements Manager
class InteractiveElements {
    constructor() {
        this.init();
    }

    init() {
        this.initProgressBar();
        this.initCountUp();
        this.initImageComparison();
        this.initVideoPlayer();
        this.initTooltips();
        this.initDropdownMenus();
        this.initTabs();
        this.initAccordion();
        this.initProgressIndicators();
        this.initImageZoom();
        this.initCopyToClipboard();
    }

    // Progress bar animations
    initProgressBar() {
        const progressBars = document.querySelectorAll('.progress-bar-fill');
        
        const progressObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const progressBar = entry.target;
                    const targetWidth = progressBar.dataset.width || 100;
                    
                    this.animateProgressBar(progressBar, targetWidth);
                    progressObserver.unobserve(progressBar);
                }
            });
        }, { threshold: 0.5 });

        progressBars.forEach(bar => {
            progressObserver.observe(bar);
        });
    }

    animateProgressBar(element, target) {
        let current = 0;
        const increment = target / 100;
        const timer = setInterval(() => {
            current += increment;
            element.style.width = Math.min(current, target) + '%';
            
            if (current >= target) {
                clearInterval(timer);
            }
        }, 20);
    }

    // Count up animations
    initCountUp() {
        const countElements = document.querySelectorAll('[data-count]');
        
        const countObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                    const element = entry.target;
                    const target = parseInt(element.dataset.count);
                    const duration = parseInt(element.dataset.duration) || 2000;
                    
                    this.countUp(element, target, duration);
                    element.classList.add('counted');
                    countObserver.unobserve(element);
                }
            });
        }, { threshold: 0.5 });

        countElements.forEach(element => {
            countObserver.observe(element);
        });
    }

    countUp(element, target, duration) {
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target.toLocaleString();
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current).toLocaleString();
            }
        }, 16);
    }

    // Before/After image comparison
    initImageComparison() {
        const comparisonContainers = document.querySelectorAll('.before-after-container');
        
        comparisonContainers.forEach(container => {
            const slider = container.querySelector('.comparison-slider');
            const beforeImage = container.querySelector('.before-image');
            const afterImage = container.querySelector('.after-image');
            
            if (slider && beforeImage && afterImage) {
                this.createImageComparison(slider, beforeImage, afterImage, container);
            }
        });
    }

    createImageComparison(slider, beforeImage, afterImage, container) {
        let isActive = false;
        const rect = container.getBoundingClientRect();
        
        const updateComparison = (clientX) => {
            const x = clientX - rect.left;
            const percentage = Math.max(0, Math.min(100, (x / rect.width) * 100));
            
            slider.style.left = percentage + '%';
            beforeImage.style.width = percentage + '%';
        };

        const startDrag = (e) => {
            isActive = true;
            document.addEventListener('mousemove', drag);
            document.addEventListener('mouseup', stopDrag);
        };

        const drag = (e) => {
            if (isActive) {
                updateComparison(e.clientX);
            }
        };

        const stopDrag = () => {
            isActive = false;
            document.removeEventListener('mousemove', drag);
            document.removeEventListener('mouseup', stopDrag);
        };

        slider.addEventListener('mousedown', startDrag);
        container.addEventListener('mousedown', (e) => {
            if (e.target === slider) return;
            updateComparison(e.clientX);
            startDrag(e);
        });
    }

    // Video player with custom controls
    initVideoPlayer() {
        const videoContainers = document.querySelectorAll('.video-container');
        
        videoContainers.forEach(container => {
            const video = container.querySelector('video');
            const playButton = container.querySelector('.play-button');
            const progressBar = container.querySelector('.video-progress');
            const volumeButton = container.querySelector('.volume-button');
            
            if (video && playButton) {
                this.createCustomVideoPlayer(video, playButton, progressBar, volumeButton, container);
            }
        });
    }

    createCustomVideoPlayer(video, playButton, progressBar, volumeButton, container) {
        // Play/Pause
        playButton.addEventListener('click', () => {
            if (video.paused) {
                video.play();
                playButton.innerHTML = '<i class="fas fa-pause"></i>';
            } else {
                video.pause();
                playButton.innerHTML = '<i class="fas fa-play"></i>';
            }
        });

        // Progress bar
        if (progressBar) {
            video.addEventListener('timeupdate', () => {
                const progress = (video.currentTime / video.duration) * 100;
                progressBar.style.width = progress + '%';
            });

            progressBar.addEventListener('click', (e) => {
                const rect = progressBar.getBoundingClientRect();
                const progress = (e.clientX - rect.left) / rect.width;
                video.currentTime = progress * video.duration;
            });
        }

        // Volume control
        if (volumeButton) {
            volumeButton.addEventListener('click', () => {
                if (video.muted) {
                    video.muted = false;
                    volumeButton.innerHTML = '<i class="fas fa-volume-up"></i>';
                } else {
                    video.muted = true;
                    volumeButton.innerHTML = '<i class="fas fa-volume-mute"></i>';
                }
            });
        }

        // Auto-hide controls
        let hideControlsTimer;
        const showControls = () => {
            container.classList.remove('hide-controls');
            clearTimeout(hideControlsTimer);
            hideControlsTimer = setTimeout(() => {
                if (!video.paused) {
                    container.classList.add('hide-controls');
                }
            }, 3000);
        };

        container.addEventListener('mousemove', showControls);
        video.addEventListener('play', showControls);
        video.addEventListener('pause', () => {
            container.classList.remove('hide-controls');
        });
    }

    // Tooltip system
    initTooltips() {
        const tooltipTriggers = document.querySelectorAll('[data-tooltip]');
        
        tooltipTriggers.forEach(trigger => {
            const text = trigger.dataset.tooltip;
            const position = trigger.dataset.position || 'top';
            
            this.createTooltip(trigger, text, position);
        });
    }

    createTooltip(trigger, text, position) {
        const tooltip = document.createElement('div');
        tooltip.className = `tooltip tooltip-${position}`;
        tooltip.textContent = text;
        tooltip.style.cssText = `
            position: absolute;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 14px;
            white-space: nowrap;
            z-index: 1000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        `;

        document.body.appendChild(tooltip);

        const showTooltip = () => {
            const rect = trigger.getBoundingClientRect();
            const tooltipRect = tooltip.getBoundingClientRect();
            
            let left = rect.left + (rect.width - tooltipRect.width) / 2;
            let top = rect.top - tooltipRect.height - 10;
            
            if (position === 'bottom') {
                top = rect.bottom + 10;
            } else if (position === 'left') {
                left = rect.left - tooltipRect.width - 10;
                top = rect.top + (rect.height - tooltipRect.height) / 2;
            } else if (position === 'right') {
                left = rect.right + 10;
                top = rect.top + (rect.height - tooltipRect.height) / 2;
            }
            
            // Ensure tooltip stays in viewport
            left = Math.max(10, Math.min(left, window.innerWidth - tooltipRect.width - 10));
            top = Math.max(10, Math.min(top, window.innerHeight - tooltipRect.height - 10));
            
            tooltip.style.left = left + 'px';
            tooltip.style.top = top + 'px';
            tooltip.style.opacity = '1';
        };

        const hideTooltip = () => {
            tooltip.style.opacity = '0';
        };

        trigger.addEventListener('mouseenter', showTooltip);
        trigger.addEventListener('mouseleave', hideTooltip);
        trigger.addEventListener('focus', showTooltip);
        trigger.addEventListener('blur', hideTooltip);
    }

    // Dropdown menus
    initDropdownMenus() {
        const dropdowns = document.querySelectorAll('.dropdown');
        
        dropdowns.forEach(dropdown => {
            const trigger = dropdown.querySelector('.dropdown-trigger');
            const menu = dropdown.querySelector('.dropdown-menu');
            
            if (trigger && menu) {
                this.createDropdown(trigger, menu, dropdown);
            }
        });
    }

    createDropdown(trigger, menu, dropdown) {
        let isOpen = false;

        const openDropdown = () => {
            isOpen = true;
            menu.classList.add('active');
            trigger.setAttribute('aria-expanded', 'true');
            
            // Position menu
            const rect = trigger.getBoundingClientRect();
            menu.style.left = '0';
            menu.style.top = rect.bottom + 'px';
        };

        const closeDropdown = () => {
            isOpen = false;
            menu.classList.remove('active');
            trigger.setAttribute('aria-expanded', 'false');
        };

        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            isOpen ? closeDropdown() : openDropdown();
        });

        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (!dropdown.contains(e.target)) {
                closeDropdown();
            }
        });

        // Close on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeDropdown();
            }
        });
    }

    // Tabs system
    initTabs() {
        const tabContainers = document.querySelectorAll('.tabs');
        
        tabContainers.forEach(container => {
            const tabs = container.querySelectorAll('.tab');
            const panels = container.querySelectorAll('.tab-panel');
            
            if (tabs.length > 0 && panels.length > 0) {
                this.createTabs(tabs, panels, container);
            }
        });
    }

    createTabs(tabs, panels, container) {
        const showTab = (index) => {
            // Remove active class from all tabs and panels
            tabs.forEach(tab => tab.classList.remove('active'));
            panels.forEach(panel => panel.classList.remove('active'));
            
            // Add active class to current tab and panel
            if (tabs[index] && panels[index]) {
                tabs[index].classList.add('active');
                panels[index].classList.add('active');
            }
        };

        tabs.forEach((tab, index) => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                showTab(index);
            });
        });
    }

    // Accordion system
    initAccordion() {
        const accordions = document.querySelectorAll('.accordion');
        
        accordions.forEach(accordion => {
            const items = accordion.querySelectorAll('.accordion-item');
            
            items.forEach(item => {
                const header = item.querySelector('.accordion-header');
                const content = item.querySelector('.accordion-content');
                
                if (header && content) {
                    this.createAccordionItem(header, content, item);
                }
            });
        });
    }

    createAccordionItem(header, content, item) {
        const toggle = () => {
            const isOpen = item.classList.contains('active');
            
            // Close all items in the accordion
            const accordion = item.closest('.accordion');
            const allItems = accordion.querySelectorAll('.accordion-item');
            allItems.forEach(allItem => {
                if (allItem !== item) {
                    allItem.classList.remove('active');
                    const allContent = allItem.querySelector('.accordion-content');
                    if (allContent) {
                        allContent.style.maxHeight = '0';
                    }
                }
            });
            
            // Toggle current item
            if (!isOpen) {
                item.classList.add('active');
                content.style.maxHeight = content.scrollHeight + 'px';
            } else {
                item.classList.remove('active');
                content.style.maxHeight = '0';
            }
        };

        header.addEventListener('click', toggle);
        header.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggle();
            }
        });
    }

    // Progress indicators
    initProgressIndicators() {
        const indicators = document.querySelectorAll('.progress-indicator');
        
        const indicatorObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const indicator = entry.target;
                    const target = parseInt(indicator.dataset.percent) || 0;
                    
                    this.animateIndicator(indicator, target);
                    indicatorObserver.unobserve(indicator);
                }
            });
        }, { threshold: 0.5 });

        indicators.forEach(indicator => {
            indicatorObserver.observe(indicator);
        });
    }

    animateIndicator(element, target) {
        const circle = element.querySelector('.progress-circle');
        const text = element.querySelector('.progress-text');
        
        if (circle) {
            const radius = parseInt(circle.getAttribute('r'));
            const circumference = 2 * Math.PI * radius;
            const offset = circumference - (target / 100) * circumference;
            
            circle.style.strokeDashoffset = offset;
        }
        
        if (text) {
            let current = 0;
            const increment = target / 50;
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    text.textContent = target + '%';
                    clearInterval(timer);
                } else {
                    text.textContent = Math.floor(current) + '%';
                }
            }, 30);
        }
    }

    // Image zoom on hover
    initImageZoom() {
        const zoomableImages = document.querySelectorAll('.zoomable-image');
        
        zoomableImages.forEach(image => {
            image.addEventListener('mouseenter', () => {
                image.style.transform = 'scale(1.1)';
            });
            
            image.addEventListener('mouseleave', () => {
                image.style.transform = 'scale(1)';
            });
        });
    }

    // Copy to clipboard
    initCopyToClipboard() {
        const copyButtons = document.querySelectorAll('[data-copy]');
        
        copyButtons.forEach(button => {
            button.addEventListener('click', async () => {
                const text = button.dataset.copy;
                
                try {
                    await navigator.clipboard.writeText(text);
                    
                    // Show success feedback
                    const originalText = button.textContent;
                    button.textContent = 'Copied!';
                    button.classList.add('copied');
                    
                    setTimeout(() => {
                        button.textContent = originalText;
                        button.classList.remove('copied');
                    }, 2000);
                } catch (err) {
                    console.error('Failed to copy text: ', err);
                }
            });
        });
    }
}

// Initialize interactive elements
document.addEventListener('DOMContentLoaded', () => {
    window.interactiveElements = new InteractiveElements();
});

// Export for use in other scripts
window.InteractiveElements = InteractiveElements;
