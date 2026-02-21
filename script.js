/**
 * LUMIRIZE Inc. - Official Website JavaScript
 * World-Class Interactive Experience
 * Accessibility-First Approach
 */

(function() {
    'use strict';

    // ============================================
    // Utility Functions
    // ============================================

    /**
     * Debounce function to limit function calls
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Check if element is in viewport
     */
    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    // ============================================
    // Mobile Navigation
    // ============================================

    function initMobileNav() {
        const navToggle = document.querySelector('.navbar__toggle');
        const navMenu = document.querySelector('.navbar__menu');
        const navLinks = document.querySelectorAll('.navbar__link');
        const body = document.body;

        if (!navToggle || !navMenu) return;

        // Toggle mobile menu
        navToggle.addEventListener('click', () => {
            const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
            navToggle.setAttribute('aria-expanded', !isExpanded);
            navMenu.classList.toggle('active');
            body.style.overflow = !isExpanded ? 'hidden' : '';

            // Update toggle button label
            navToggle.setAttribute('aria-label', 
                !isExpanded ? 'メニューを閉じる' : 'メニューを開く'
            );
        });

        // Close menu when clicking on nav links
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navToggle.setAttribute('aria-expanded', 'false');
                navMenu.classList.remove('active');
                body.style.overflow = '';
                navToggle.setAttribute('aria-label', 'メニューを開く');
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!navMenu.contains(e.target) && !navToggle.contains(e.target)) {
                if (navMenu.classList.contains('active')) {
                    navToggle.setAttribute('aria-expanded', 'false');
                    navMenu.classList.remove('active');
                    body.style.overflow = '';
                    navToggle.setAttribute('aria-label', 'メニューを開く');
                }
            }
        });

        // Close menu on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navMenu.classList.contains('active')) {
                navToggle.setAttribute('aria-expanded', 'false');
                navMenu.classList.remove('active');
                body.style.overflow = '';
                navToggle.setAttribute('aria-label', 'メニューを開く');
                navToggle.focus();
            }
        });
    }

    // ============================================
    // Sticky Header on Scroll
    // ============================================

    function initStickyHeader() {
        const header = document.querySelector('.header');
        if (!header) return;

        const handleScroll = debounce(() => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }, 10);

        window.addEventListener('scroll', handleScroll);
    }

    // ============================================
    // Smooth Scroll for Anchor Links
    // ============================================

    function initSmoothScroll() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#' || href === '#!') return;

                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    const headerOffset = 80;
                    const elementPosition = target.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });

                    // Update focus for accessibility
                    target.setAttribute('tabindex', '-1');
                    target.focus();
                    
                    // Update URL
                    history.pushState(null, null, href);
                }
            });
        });
    }

    // ============================================
    // FAQ Accordion
    // ============================================

    function initFAQ() {
        const faqButtons = document.querySelectorAll('.faq-item__question');

        faqButtons.forEach(button => {
            button.addEventListener('click', () => {
                const expanded = button.getAttribute('aria-expanded') === 'true';
                const answerId = button.getAttribute('aria-controls');
                const answer = document.getElementById(answerId);

                // Close all other accordions
                faqButtons.forEach(otherButton => {
                    if (otherButton !== button) {
                        otherButton.setAttribute('aria-expanded', 'false');
                        const otherAnswerId = otherButton.getAttribute('aria-controls');
                        const otherAnswer = document.getElementById(otherAnswerId);
                        if (otherAnswer) {
                            otherAnswer.setAttribute('aria-hidden', 'true');
                        }
                    }
                });

                // Toggle current accordion
                button.setAttribute('aria-expanded', !expanded);
                if (answer) {
                    answer.setAttribute('aria-hidden', expanded);
                }
            });

            // Keyboard accessibility
            button.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    button.click();
                }
            });
        });
    }

    // ============================================
    // Contact Form Validation & Submission
    // ============================================

    function initContactForm() {
        const form = document.getElementById('contact-form');
        if (!form) return;

        const nameInput = document.getElementById('name');
        const emailInput = document.getElementById('email');
        const phoneInput = document.getElementById('phone');
        const inquiryTypeSelect = document.getElementById('inquiry-type');
        const messageTextarea = document.getElementById('message');
        const privacyCheckbox = document.getElementById('privacy');

        // Validation functions
        function validateName(value) {
            if (!value.trim()) {
                return 'お名前を入力してください。';
            }
            if (value.trim().length < 2) {
                return 'お名前は2文字以上で入力してください。';
            }
            return '';
        }

        function validateEmail(value) {
            if (!value.trim()) {
                return 'メールアドレスを入力してください。';
            }
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                return '有効なメールアドレスを入力してください。';
            }
            return '';
        }

        function validatePhone(value) {
            if (value.trim() && !/^[0-9\-\+\(\)\s]+$/.test(value)) {
                return '有効な電話番号を入力してください。';
            }
            return '';
        }

        function validateInquiryType(value) {
            if (!value) {
                return '相談内容を選択してください。';
            }
            return '';
        }

        function validateMessage(value) {
            if (!value.trim()) {
                return 'お問い合わせ内容を入力してください。';
            }
            if (value.trim().length < 10) {
                return 'お問い合わせ内容は10文字以上で入力してください。';
            }
            return '';
        }

        function validatePrivacy(checked) {
            if (!checked) {
                return 'プライバシーポリシーに同意してください。';
            }
            return '';
        }

        function showError(input, message) {
            const errorElement = document.getElementById(input.id + '-error');
            if (errorElement) {
                errorElement.textContent = message;
                input.classList.add('error');
                input.setAttribute('aria-invalid', 'true');
            }
        }

        function clearError(input) {
            const errorElement = document.getElementById(input.id + '-error');
            if (errorElement) {
                errorElement.textContent = '';
                input.classList.remove('error');
                input.setAttribute('aria-invalid', 'false');
            }
        }

        // Real-time validation
        nameInput.addEventListener('blur', () => {
            const error = validateName(nameInput.value);
            if (error) {
                showError(nameInput, error);
            } else {
                clearError(nameInput);
            }
        });

        nameInput.addEventListener('input', () => {
            if (nameInput.classList.contains('error')) {
                const error = validateName(nameInput.value);
                if (!error) {
                    clearError(nameInput);
                }
            }
        });

        emailInput.addEventListener('blur', () => {
            const error = validateEmail(emailInput.value);
            if (error) {
                showError(emailInput, error);
            } else {
                clearError(emailInput);
            }
        });

        emailInput.addEventListener('input', () => {
            if (emailInput.classList.contains('error')) {
                const error = validateEmail(emailInput.value);
                if (!error) {
                    clearError(emailInput);
                }
            }
        });

        phoneInput.addEventListener('blur', () => {
            const error = validatePhone(phoneInput.value);
            if (error) {
                showError(phoneInput, error);
            } else {
                clearError(phoneInput);
            }
        });

        inquiryTypeSelect.addEventListener('change', () => {
            const error = validateInquiryType(inquiryTypeSelect.value);
            if (error) {
                showError(inquiryTypeSelect, error);
            } else {
                clearError(inquiryTypeSelect);
            }
        });

        messageTextarea.addEventListener('blur', () => {
            const error = validateMessage(messageTextarea.value);
            if (error) {
                showError(messageTextarea, error);
            } else {
                clearError(messageTextarea);
            }
        });

        privacyCheckbox.addEventListener('change', () => {
            const error = validatePrivacy(privacyCheckbox.checked);
            if (error) {
                showError(privacyCheckbox, error);
            } else {
                clearError(privacyCheckbox);
            }
        });

        // Form submission
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            // Validate all fields
            const nameError = validateName(nameInput.value);
            const emailError = validateEmail(emailInput.value);
            const phoneError = validatePhone(phoneInput.value);
            const inquiryTypeError = validateInquiryType(inquiryTypeSelect.value);
            const messageError = validateMessage(messageTextarea.value);
            const privacyError = validatePrivacy(privacyCheckbox.checked);

            // Show errors
            if (nameError) showError(nameInput, nameError);
            else clearError(nameInput);

            if (emailError) showError(emailInput, emailError);
            else clearError(emailInput);

            if (phoneError) showError(phoneInput, phoneError);
            else clearError(phoneInput);

            if (inquiryTypeError) showError(inquiryTypeSelect, inquiryTypeError);
            else clearError(inquiryTypeSelect);

            if (messageError) showError(messageTextarea, messageError);
            else clearError(messageTextarea);

            if (privacyError) showError(privacyCheckbox, privacyError);
            else clearError(privacyCheckbox);

            // Check if there are any errors
            if (nameError || emailError || phoneError || inquiryTypeError || messageError || privacyError) {
                // Focus on first error
                if (nameError) nameInput.focus();
                else if (emailError) emailInput.focus();
                else if (phoneError) phoneInput.focus();
                else if (inquiryTypeError) inquiryTypeSelect.focus();
                else if (messageError) messageTextarea.focus();
                else if (privacyError) privacyCheckbox.focus();
                return;
            }

            // If validation passes, show success message
            // In a real application, you would send the data to a server here
            const successMessage = document.getElementById('form-success');
            if (successMessage) {
                successMessage.style.display = 'flex';
                form.reset();
                
                // Scroll to success message
                successMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                
                // Hide success message after 10 seconds
                setTimeout(() => {
                    successMessage.style.display = 'none';
                }, 10000);
            }

            // Log form data (for development)
            console.log('Form submitted:', {
                name: nameInput.value,
                email: emailInput.value,
                phone: phoneInput.value,
                inquiryType: inquiryTypeSelect.value,
                message: messageTextarea.value,
                privacy: privacyCheckbox.checked
            });
        });
    }

    // ============================================
    // Back to Top Button
    // ============================================

    function initBackToTop() {
        const backToTopButton = document.getElementById('back-to-top');
        if (!backToTopButton) return;

        const handleScroll = debounce(() => {
            if (window.scrollY > 500) {
                backToTopButton.classList.add('visible');
                backToTopButton.style.display = 'flex';
            } else {
                backToTopButton.classList.remove('visible');
                setTimeout(() => {
                    if (!backToTopButton.classList.contains('visible')) {
                        backToTopButton.style.display = 'none';
                    }
                }, 300);
            }
        }, 100);

        window.addEventListener('scroll', handleScroll);

        backToTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        // Keyboard accessibility
        backToTopButton.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            }
        });
    }

    // ============================================
    // Intersection Observer for Scroll Animations
    // ============================================

    function initScrollAnimations() {
        // Check if user prefers reduced motion
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (prefersReducedMotion) return;

        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Observe elements with fade-in class
        const elementsToAnimate = document.querySelectorAll('.fade-in');
        elementsToAnimate.forEach(el => observer.observe(el));

        // Add fade-in class to specific elements
        const animateElements = [
            '.stat-card',
            '.info-grid__item',
            '.profile-card',
            '.philosophy-card',
            '.service-card',
            '.process-step',
            '.faq-item',
            '.contact-card'
        ];

        animateElements.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach((el, index) => {
                el.classList.add('fade-in');
                el.style.transitionDelay = `${index * 0.1}s`;
            });
        });

        // Re-observe all fade-in elements
        const allFadeInElements = document.querySelectorAll('.fade-in');
        allFadeInElements.forEach(el => observer.observe(el));
    }

    // ============================================
    // Active Navigation Link on Scroll
    // ============================================

    function initActiveNavigation() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.navbar__link[href^="#"]');

        const handleScroll = debounce(() => {
            let current = '';
            const scrollPosition = window.scrollY + 100;

            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;

                if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('active');
                const href = link.getAttribute('href');
                if (href === `#${current}`) {
                    link.classList.add('active');
                }
            });
        }, 100);

        window.addEventListener('scroll', handleScroll);
    }

    // ============================================
    // Accessible Focus Management
    // ============================================

    function initFocusManagement() {
        // Add focus-visible class for keyboard navigation
        let isUsingKeyboard = false;

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                isUsingKeyboard = true;
                document.body.classList.add('keyboard-nav');
            }
        });

        document.addEventListener('mousedown', () => {
            isUsingKeyboard = false;
            document.body.classList.remove('keyboard-nav');
        });

        // Skip to main content functionality
        const skipLink = document.querySelector('.skip-link');
        if (skipLink) {
            skipLink.addEventListener('click', (e) => {
                e.preventDefault();
                const mainContent = document.getElementById('main-content');
                if (mainContent) {
                    mainContent.setAttribute('tabindex', '-1');
                    mainContent.focus();
                    mainContent.addEventListener('blur', () => {
                        mainContent.removeAttribute('tabindex');
                    }, { once: true });
                }
            });
        }
    }

    // ============================================
    // Performance: Lazy Loading Images
    // ============================================

    function initLazyLoading() {
        if ('loading' in HTMLImageElement.prototype) {
            const images = document.querySelectorAll('img[loading="lazy"]');
            images.forEach(img => {
                img.src = img.dataset.src || img.src;
            });
        } else {
            // Fallback for browsers that don't support lazy loading
            const script = document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/lazysizes/5.3.2/lazysizes.min.js';
            document.body.appendChild(script);
        }
    }

    // ============================================
    // Initialize All Functions
    // ============================================

    function init() {
        // DOM content loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initAll);
        } else {
            initAll();
        }
    }

    function initAll() {
        console.log('🚀 LUMIRIZE Inc. Website Initialized');
        
        initMobileNav();
        initStickyHeader();
        initSmoothScroll();
        initFAQ();
        initContactForm();
        initBackToTop();
        initScrollAnimations();
        initActiveNavigation();
        initFocusManagement();
        initLazyLoading();

        // Log for accessibility testing
        console.log('✅ All interactive features initialized with accessibility support');
    }

    // Start initialization
    init();

    // ============================================
    // Service Worker Registration (Optional)
    // ============================================

    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            // Uncomment when you have a service worker file
            // navigator.serviceWorker.register('/sw.js')
            //     .then(registration => {
            //         console.log('✅ ServiceWorker registered:', registration);
            //     })
            //     .catch(error => {
            //         console.log('❌ ServiceWorker registration failed:', error);
            //     });
        });
    }

})();
