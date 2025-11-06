document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for navigation links (if any were added)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Accordion functionality for FAQ
    const accordionHeaders = document.querySelectorAll('.accordion-header');

    accordionHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const accordionItem = header.parentElement;
            const accordionContent = header.nextElementSibling;

            // Close other open accordions
            accordionHeaders.forEach(otherHeader => {
                if (otherHeader !== header) {
                    otherHeader.classList.remove('active');
                    otherHeader.nextElementSibling.style.maxHeight = 0;
                    otherHeader.parentElement.classList.remove('active');
                }
            });

            accordionItem.classList.toggle('active');
            header.classList.toggle('active');

            if (accordionItem.classList.contains('active')) {
                accordionContent.style.maxHeight = accordionContent.scrollHeight + 'px';
            } else {
                accordionContent.style.maxHeight = 0;
            }
        });
    });

    // Scroll animations
    const animateOnScrollElements = document.querySelectorAll('.features-section h2, .feature-item, .how-it-works-section h2, .step-item, .testimonials-section h2, .testimonial-item, .faq-section h2, .accordion-item');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
                entry.target.classList.remove('hidden');
            } else {
                // Optional: remove 'show' class when out of view to re-trigger on scroll back
                // entry.target.classList.remove('show');
                // entry.target.classList.add('hidden');
            }
        });
    }, {
        threshold: 0.1, // Trigger when 10% of the item is visible
        rootMargin: '0px 0px -50px 0px' // Adjust when the animation triggers
    });

    animateOnScrollElements.forEach(el => {
        el.classList.add('hidden'); // Add hidden class initially
        observer.observe(el);
    });

    // Add pulse animation to CTA button
    const ctaButton = document.querySelector('.cta-button');
    if (ctaButton) {
        ctaButton.style.animation = 'pulse 2s infinite';
    }

    // Adjust accordion content max-height on window resize
    window.addEventListener('resize', () => {
        accordionHeaders.forEach(header => {
            const accordionItem = header.parentElement;
            const accordionContent = header.nextElementSibling;
            if (accordionItem.classList.contains('active')) {
                accordionContent.style.maxHeight = accordionContent.scrollHeight + 'px';
            }
        });
    });
});
