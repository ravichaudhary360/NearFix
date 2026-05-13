// ═══════════════════════════════════════
//  NEARFIX — MAIN JS
// ═══════════════════════════════════════

// Auto dismiss alerts
document.addEventListener('DOMContentLoaded', () => {

    // Dismiss alerts after 3.5s
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(a => {
            a.style.transition = 'opacity 0.4s';
            a.style.opacity = '0';
            setTimeout(() => a.remove(), 400);
        });
    }, 3500);

    // Active nav link highlight
    const path = window.location.pathname;
    document.querySelectorAll('.nf-nav-link').forEach(link => {
        if (link.getAttribute('href') === path) {
            link.classList.add('active');
        }
    });

    // Photo preview on upload
    const photoInput = document.getElementById('photoInput');
    if (photoInput) {
        photoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = document.getElementById('photoPreview');
                if (preview) {
                    preview.innerHTML = `<img src="${e.target.result}" style="width:100%;height:100%;object-fit:cover;border-radius:inherit;">`;
                }
            };
            reader.readAsDataURL(file);
        });
    }

    // Experience slider value display
    const expSlider = document.querySelector('.nf-exp-slider');
    if (expSlider) {
        const expVal = document.getElementById('expVal');
        expSlider.addEventListener('input', function() {
            if (expVal) expVal.textContent = this.value + ' yrs';
        });
    }

});

// Location detection
function detectLocation() {
    const btn = document.querySelector('.nf-location-btn');
    if (!btn) return;
    btn.textContent = '📍 Detecting...';
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            () => { btn.textContent = '✅ Location detected!'; btn.style.color = '#1D9E75'; },
            () => { btn.textContent = '❌ Location access denied'; }
        );
    }
}

// Payment method selector
function selectMethod(method, el) {
    document.querySelectorAll('.nf-pay-method').forEach(m => m.classList.remove('selected'));
    el.classList.add('selected');
    const input = document.getElementById('payMethodInput');
    if (input) input.value = method;
}

// Star rating
const ratingLabels = ['', 'Terrible 😞', 'Bad 😕', 'Okay 😐', 'Good 😊', 'Excellent! 🔥'];
function setRating(val) {
    const input = document.getElementById('ratingInput');
    const label = document.getElementById('ratingLabel');
    if (input) input.value = val;
    if (label) label.textContent = ratingLabels[val];
    document.querySelectorAll('.nf-star').forEach((s, i) => {
        s.classList.toggle('active', i < val);
    });
}

// Provider availability toggle
function toggleAvailability() {
    const btn = document.getElementById('availToggle');
    if (btn) btn.classList.toggle('on');
}