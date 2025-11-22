// ==================== 
// SecurePass Vault - Main JavaScript
// ==================== 

'use strict';

// ==================== 
// Theme Toggle Functionality
// ==================== 
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

// Check for saved theme preference or default to light mode
const currentTheme = localStorage.getItem('theme') || 'light';
if (currentTheme === 'dark') {
    body.classList.add('dark-theme');
    themeToggle.textContent = '☀️';
}

// Toggle theme on button click
themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-theme');
    
    // Update button icon and save preference
    if (body.classList.contains('dark-theme')) {
        themeToggle.textContent = '☀️';
        localStorage.setItem('theme', 'dark');
    } else {
        themeToggle.textContent = '🌙';
        localStorage.setItem('theme', 'light');
    }
});

// ==================== 
// Mobile Navigation
// ==================== 
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

// Toggle mobile menu
hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when a link is clicked
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    }
});

// ==================== 
// Smooth Scrolling for Navigation Links
// ==================== 
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        
        if (target) {
            const headerOffset = 80; // Height of fixed header
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// ==================== 
// Scroll to Top Button
// ==================== 
const scrollTopBtn = document.createElement('button');
scrollTopBtn.className = 'scroll-top';
scrollTopBtn.innerHTML = '↑';
scrollTopBtn.setAttribute('aria-label', 'Scroll to top');
document.body.appendChild(scrollTopBtn);

// Show/hide scroll to top button based on scroll position
window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        scrollTopBtn.classList.add('visible');
    } else {
        scrollTopBtn.classList.remove('visible');
    }
});

// Scroll to top when button is clicked
scrollTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// ==================== 
// Header Shadow on Scroll
// ==================== 
window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    if (window.scrollY > 100) {
        header.style.boxShadow = '0 4px 20px rgba(0,0,0,0.15)';
    } else {
        header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
    }
});

// ==================== 
// Active Navigation Link Highlighting
// ==================== 
window.addEventListener('scroll', () => {
    let current = '';
    const sections = document.querySelectorAll('section');
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        if (pageYOffset >= (sectionTop - 200)) {
            current = section.getAttribute('id');
        }
    });

    // Remove active class from all links
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.classList.remove('active');
        
        // Add active class to current section link
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// ==================== 
// Scroll Animation Observer
// ==================== 
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // Add fade-in animation
            entry.target.style.opacity = '0';
            entry.target.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                entry.target.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }, 100);
            
            // Stop observing after animation
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe elements for scroll animation
document.querySelectorAll('.feature-card, .step, .security-item, .reason, .testimonial').forEach(el => {
    observer.observe(el);
});

// ==================== 
// Copy to Clipboard Function
// ==================== 
function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copied to clipboard!', 'success');
        }).catch(err => {
            console.error('Failed to copy:', err);
            showNotification('Failed to copy', 'error');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            document.execCommand('copy');
            showNotification('Copied to clipboard!', 'success');
        } catch (err) {
            console.error('Failed to copy:', err);
            showNotification('Failed to copy', 'error');
        }
        
        document.body.removeChild(textArea);
    }
}

// ==================== 
// Notification System
// ==================== 
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Styling
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        animation: slideIn 0.3s ease;
        min-width: 250px;
        font-weight: 500;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ==================== 
// Form Validation (if forms are added)
// ==================== 
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const email = form.querySelector('input[type="email"]');
    
    if (email && !validateEmail(email.value)) {
        showNotification('Please enter a valid email address', 'error');
        email.focus();
        return;
    }
    
    // Show success message
    showNotification('Thank you for your submission!', 'success');
    form.reset();
}

// Add form submit listeners if forms exist
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', handleFormSubmit);
});

// ==================== 
// Lazy Loading Images
// ==================== 
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                
                if (img.dataset.srcset) {
                    img.srcset = img.dataset.srcset;
                    img.removeAttribute('data-srcset');
                }
                
                observer.unobserve(img);
            }
        });
    });
    
    // Observe all images with data-src attribute
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ==================== 
// Detect Browser & Device
// ==================== 
function detectBrowser() {
    const userAgent = navigator.userAgent;
    let browser = 'Unknown';
    
    if (userAgent.indexOf('Firefox') > -1) {
        browser = 'Firefox';
    } else if (userAgent.indexOf('Chrome') > -1) {
        browser = 'Chrome';
    } else if (userAgent.indexOf('Safari') > -1) {
        browser = 'Safari';
    } else if (userAgent.indexOf('Edge') > -1) {
        browser = 'Edge';
    } else if (userAgent.indexOf('Opera') > -1 || userAgent.indexOf('OPR') > -1) {
        browser = 'Opera';
    }
    
    return browser;
}

function isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

function isTablet() {
    return /(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(navigator.userAgent);
}

// Log device info (for debugging)
console.log('Browser:', detectBrowser());
console.log('Mobile:', isMobile());
console.log('Tablet:', isTablet());

// ==================== 
// Performance Monitoring
// ==================== 
window.addEventListener('load', () => {
    // Log page load time
    if (window.performance && window.performance.timing) {
        const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
        console.log(`Page loaded in ${loadTime}ms`);
    }
    
    // Log DOM content loaded time
    if (window.performance && window.performance.timing) {
        const domTime = window.performance.timing.domContentLoadedEventEnd - window.performance.timing.navigationStart;
        console.log(`DOM ready in ${domTime}ms`);
    }
});

// ==================== 
// Keyboard Navigation Shortcuts
// ==================== 
document.addEventListener('keydown', (e) => {
    // ESC key - Close mobile menu
    if (e.key === 'Escape') {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    }
    
    // Ctrl/Cmd + K - Quick search (if search is implemented)
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        // Implement search functionality here
        console.log('Search shortcut triggered');
    }
    
    // Arrow Up - Scroll to top
    if (e.key === 'Home') {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    // Arrow Down - Scroll to bottom
    if (e.key === 'End') {
        e.preventDefault();
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }
});

// ==================== 
// Auto-update Copyright Year
// ==================== 
document.addEventListener('DOMContentLoaded', () => {
    const yearElement = document.querySelector('.footer-bottom p');
    if (yearElement) {
        const currentYear = new Date().getFullYear();
        yearElement.innerHTML = yearElement.innerHTML.replace(/\d{4}/, currentYear);
    }
});

// ==================== 
// Print Page Function
// ==================== 
function printPage() {
    window.print();
}

// ==================== 
// Share Page Function
// ==================== 
async function sharePage() {
    const shareData = {
        title: document.title,
        text: 'Check out SecurePass Vault - A secure password manager',
        url: window.location.href
    };
    
    // Check if Web Share API is supported
    if (navigator.share) {
        try {
            await navigator.share(shareData);
            console.log('Page shared successfully');
        } catch (err) {
            if (err.name !== 'AbortError') {
                console.log('Error sharing:', err);
                copyToClipboard(window.location.href);
            }
        }
    } else {
        // Fallback - Copy URL to clipboard
        copyToClipboard(window.location.href);
    }
}

// ==================== 
// Stats Counter Animation
// ==================== 
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16); // 60 FPS
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

// Animate stat numbers when they come into view
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statNumber = entry.target.querySelector('.stat-number');
            if (statNumber && !statNumber.dataset.animated) {
                const targetValue = parseInt(statNumber.textContent.replace(/,/g, ''));
                if (!isNaN(targetValue)) {
                    animateCounter(statNumber, targetValue);
                    statNumber.dataset.animated = 'true';
                }
            }
        }
    });
}, { threshold: 0.5 });

// Observe stat items
document.querySelectorAll('.stat-item').forEach(item => {
    statsObserver.observe(item);
});

// ==================== 
// Prevent Animation on Page Load
// ==================== 
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

// ==================== 
// External Links - Open in New Tab
// ==================== 
document.querySelectorAll('a[href^="http"]').forEach(link => {
    if (link.hostname !== window.location.hostname) {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    }
});

// ==================== 
// Prevent Empty Anchor Links
// ==================== 
document.querySelectorAll('a[href="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
    });
});

// ==================== 
// Service Worker Registration (for PWA support)
// ==================== 
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment when you create a service worker file
        // navigator.serviceWorker.register('/service-worker.js')
        //     .then(registration => {
        //         console.log('ServiceWorker registered:', registration);
        //     })
        //     .catch(error => {
        //         console.log('ServiceWorker registration failed:', error);
        //     });
    });
}

// ==================== 
// Online/Offline Detection
// ==================== 
window.addEventListener('online', () => {
    showNotification('You are back online!', 'success');
});

window.addEventListener('offline', () => {
    showNotification('You are offline', 'error');
});

// ==================== 
// Console Welcome Message
// ==================== 
console.log('%c🔐 SecurePass Vault', 'color: #667eea; font-size: 24px; font-weight: bold;');
console.log('%cOpen-source password manager with zero-knowledge encryption', 'color: #764ba2; font-size: 14px;');
console.log('%cBuilt with ❤️ and security in mind', 'color: #666; font-size: 12px;');
console.log('%c\nInterested in the code? Check out our GitHub repository!', 'color: #10b981; font-size: 12px;');

// ==================== 
// Debug Mode (remove in production)
// ==================== 
const DEBUG_MODE = false; // Set to false for production

if (DEBUG_MODE) {
    console.log('Debug mode enabled');
    
    // Log all clicks
    document.addEventListener('click', (e) => {
        console.log('Clicked:', e.target);
    });
    
    // Log all scroll events
    let scrollTimeout;
    window.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            console.log('Scroll position:', window.pageYOffset);
        }, 100);
    });
}

// ==================== 
// Feature Detection
// ==================== 
const features = {
    localStorage: typeof(Storage) !== 'undefined',
    serviceWorker: 'serviceWorker' in navigator,
    webShare: 'share' in navigator,
    intersectionObserver: 'IntersectionObserver' in window,
    clipboard: navigator.clipboard !== undefined
};

if (DEBUG_MODE) {
    console.log('Browser features:', features);
}

// ==================== 
// Error Handling
// ==================== 
window.addEventListener('error', (e) => {
    console.error('Global error:', e.error);
    
    // In production, you might want to send errors to a logging service
    // sendErrorToLoggingService(e.error);
});

window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled promise rejection:', e.reason);
    
    // In production, you might want to send errors to a logging service
    // sendErrorToLoggingService(e.reason);
});

// ==================== 
// Page Visibility API - Pause animations when tab is hidden
// ==================== 
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        console.log('Tab is hidden');
        // Pause heavy animations or operations
    } else {
        console.log('Tab is visible');
        // Resume animations or operations
    }
});

// ==================== 
// Utility Functions
// ==================== 

// Debounce function for performance optimization
function debounce(func, wait = 300) {
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

// Throttle function for performance optimization
function throttle(func, limit = 300) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Example usage of debounce on window resize
const handleResize = debounce(() => {
    console.log('Window resized:', window.innerWidth, 'x', window.innerHeight);
}, 300);

window.addEventListener('resize', handleResize);

// ==================== 
// Initialize Everything
// ==================== 
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed');
    
    // Add any initialization code here
    
    // Check if user prefers reduced motion
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        console.log('User prefers reduced motion');
        // Disable or reduce animations
    }
    
    // Log initial theme
    console.log('Current theme:', localStorage.getItem('theme') || 'light');
});

// ==================== 
// Export functions (if using modules)
// ==================== 
// Uncomment if using ES6 modules
// export { 
//     copyToClipboard, 
//     showNotification, 
//     validateEmail, 
//     sharePage, 
//     printPage 
// };
