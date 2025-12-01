document.addEventListener('DOMContentLoaded', function() {
    
    // ========== AUTO-HIDE ALERTS ==========
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (!alert.classList.contains('alert-permanent')) {
            setTimeout(() => {
                alert.style.transition = 'opacity 0.5s';
                alert.style.opacity = '0';
                setTimeout(() => {
                    alert.remove();
                }, 500);
            }, 5000); // Hide after 5 seconds
        }
    });

    // ========== SEARCH TABS FUNCTIONALITY ==========
    const searchTabs = document.querySelectorAll('.search-tab');
    searchTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs
            searchTabs.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Get tab type
            const tabType = this.getAttribute('data-tab');
            console.log('Selected tab:', tabType);
            
            // You can add different search functionality here
            // For example, change the search endpoint based on tab
        });
    });

    // ========== CONFIRM DELETE ACTIONS ==========
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Are you sure you want to delete this?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // ========== FORM VALIDATION ==========
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // ========== LOADING SPINNER FOR BUTTONS ==========
    const loadingButtons = document.querySelectorAll('[data-loading]');
    loadingButtons.forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Loading...';
            this.disabled = true;

            // Re-enable after 3 seconds (adjust based on your needs)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 3000);
        });
    });

    // ========== TOOLTIPS INITIALIZATION ==========
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ========== SMOOTH SCROLL ==========
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // ========== TABLE ROW CLICK ==========
    const clickableRows = document.querySelectorAll('tr[data-href]');
    clickableRows.forEach(row => {
        row.addEventListener('click', function(e) {
            if (e.target.tagName !== 'A' && e.target.tagName !== 'BUTTON') {
                window.location.href = this.getAttribute('data-href');
            }
        });
        row.style.cursor = 'pointer';
    });

    // ========== SEARCH INPUT ENHANCEMENT ==========
    const searchInputs = document.querySelectorAll('input[type="search"], input.search-box');
    searchInputs.forEach(input => {
        // Add clear button
        const clearBtn = document.createElement('button');
        clearBtn.type = 'button';
        clearBtn.className = 'btn btn-sm btn-outline-secondary position-absolute end-0 top-50 translate-middle-y me-2';
        clearBtn.innerHTML = '<i class="bi bi-x"></i>';
        clearBtn.style.display = 'none';

        input.parentElement.style.position = 'relative';
        input.parentElement.appendChild(clearBtn);

        input.addEventListener('input', function() {
            clearBtn.style.display = this.value ? 'block' : 'none';
        });

        clearBtn.addEventListener('click', function() {
            input.value = '';
            input.focus();
            clearBtn.style.display = 'none';
        });
    });

    // ========== IMAGE PREVIEW FOR FILE UPLOADS ==========
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Create or update preview
                    let preview = input.parentElement.querySelector('.image-preview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.className = 'image-preview mt-2';
                        preview.style.maxWidth = '200px';
                        preview.style.maxHeight = '200px';
                        preview.style.borderRadius = '8px';
                        input.parentElement.appendChild(preview);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // ========== COPY TO CLIPBOARD ==========
    const copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Show success feedback
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="bi bi-check"></i> Copied!';
                setTimeout(() => {
                    this.innerHTML = originalText;
                }, 2000);
            });
        });
    });

    // ========== BACK TO TOP BUTTON ==========
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i class="bi bi-arrow-up"></i>';
    backToTopButton.className = 'btn btn-primary position-fixed bottom-0 end-0 m-4';
    backToTopButton.style.display = 'none';
    backToTopButton.style.zIndex = '9999';
    backToTopButton.style.borderRadius = '50%';
    backToTopButton.style.width = '50px';
    backToTopButton.style.height = '50px';
    document.body.appendChild(backToTopButton);

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });

    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // ========== PREVENT DOUBLE FORM SUBMISSION ==========
    const submitForms = document.querySelectorAll('form[data-prevent-double-submit]');
    submitForms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';
            }
        });
    });

    // ========== AUTO-REFRESH DATA ==========
    if (document.querySelector('[data-auto-refresh]')) {
        setInterval(() => {
            location.reload();
        }, 60000); // Refresh every 60 seconds
    }

    // ========== PRINT FUNCTIONALITY ==========
    const printButtons = document.querySelectorAll('[data-print]');
    printButtons.forEach(button => {
        button.addEventListener('click', function() {
            window.print();
        });
    });

    // ========== DARK MODE TOGGLE (Optional) ==========
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        // Check for saved preference
        const darkMode = localStorage.getItem('darkMode');
        if (darkMode === 'enabled') {
            document.body.classList.add('dark-mode');
        }

        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            
            // Save preference
            if (document.body.classList.contains('dark-mode')) {
                localStorage.setItem('darkMode', 'enabled');
            } else {
                localStorage.setItem('darkMode', 'disabled');
            }
        });
    }

    // ========== FORM AUTO-SAVE (Optional) ==========
    const autoSaveForms = document.querySelectorAll('[data-auto-save]');
    autoSaveForms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            // Load saved value
            const savedValue = localStorage.getItem(`form_${form.id}_${input.name}`);
            if (savedValue) {
                input.value = savedValue;
            }

            // Save on input
            input.addEventListener('input', function() {
                localStorage.setItem(`form_${form.id}_${input.name}`, this.value);
            });
        });

        // Clear on submit
        form.addEventListener('submit', function() {
            inputs.forEach(input => {
                localStorage.removeItem(`form_${form.id}_${input.name}`);
            });
        });
    });

    // ========== ANIMATION ON SCROLL ==========
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animateElements = document.querySelectorAll('.card, .stat-card');
    animateElements.forEach(el => observer.observe(el));

    console.log('Library Management System - JavaScript loaded successfully!');
});

// ========== UTILITY FUNCTIONS ==========

// Format currency
function formatCurrency(amount) {
    return '৳' + parseFloat(amount).toFixed(2);
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Confirm action
function confirmAction(message) {
    return confirm(message || 'Are you sure?');
}

// Export functions for use in other scripts
window.libraryUtils = {
    formatCurrency,
    formatDate,
    showNotification,
    confirmAction
};