// Graph Animations
function animateGraph(graphDivId) {
    const graphDiv = document.getElementById(graphDivId);
    if (graphDiv) {
        Plotly.animate(graphDiv, {
            data: [],
            traces: [0],
            layout: {}
        }, {
            transition: {
                duration: 500,
                easing: 'cubic-in-out'
            },
            frame: { duration: 500 }
        });
    }
}

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menuToggle');
    const navLinks = document.getElementById('navLinks');

    // Toggle mobile menu
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('show');
    });

    // Close menu when link clicked
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('show');
        });
    });

    // Active link highlighting
    const currentUrl = window.location.pathname;
    document.querySelectorAll('.nav-links li a').forEach(link => {
        if (link.getAttribute('href') === currentUrl) {
            link.classList.add('active');
        }
    });

    // Deforestation slider value display
    const deforestationSlider = document.getElementById('deforestation_factor');
    const deforestationValue = document.getElementById('deforestation_value');
    if (deforestationSlider) {
        deforestationSlider.addEventListener('input', () => {
            deforestationValue.textContent = Math.round(deforestationSlider.value * 100) + "%";
        });
    }

    // Disable form buttons after submit
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', (e) => {
            const btn = form.querySelector('button[type="submit"]');
            if (btn) {
                btn.disabled = true;
                btn.innerText = "Processing...";
                showLoader();
            }
        });
    });

    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Initialize graph animations
    window.onload = () => {
        ['tempGraph', 'rainGraph', 'humGraph'].forEach(id => {
            if (document.getElementById(id)) animateGraph(id);
        });
    };
});

// Loader functions
function showLoader() {
    document.getElementById('loader').classList.remove('hidden');
}
function hideLoader() {
    document.getElementById('loader').classList.add('hidden');
}

// Toast notification
function showToast(message) {
    const toast = document.getElementById('toast');
    toast.innerText = message;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), 3000);
}

// Keyboard accessibility
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.getElementById('navLinks').classList.remove('show');
    }
});