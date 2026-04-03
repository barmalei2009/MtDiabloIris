// Gallery dynamic rendering
document.addEventListener('DOMContentLoaded', function() {
  const galleryRoot = document.getElementById('gallery-root');
  if (!galleryRoot) return;
  fetch('../files/images.json')
    .then(response => response.json())
    .then(images => {
      // Group images by category
      const categories = {};
      images.forEach(img => {
        if (!categories[img.category]) categories[img.category] = [];
        categories[img.category].push(img);
      });
      // Render each category
      galleryRoot.innerHTML = Object.keys(categories).map(category => {
        const items = categories[category].map(img => `
          <article class="gallery-item">
            <img src="../images/${img.filename}" alt="${img.alt}">
            <div class="gallery-metadata">
              <span class="iris-class">${img.class}</span>
              <h4>${img.title}</h4>
            </div>
          </article>
        `).join('');
        return `
          <section class="gallery-section">
            <h3 class="gallery-category">${category}</h3>
            <div class="gallery-grid">
              ${items}
            </div>
          </section>
        `;
      }).join('');
    })
    .catch(err => {
      galleryRoot.innerHTML = '<p>Could not load gallery images.</p>';
      console.error('Gallery load error:', err);
    });
});
// Scroll Reveal Animation
const revealElements = document.querySelectorAll('.reveal');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      // Optionally stop observing after revealing
      observer.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.1,
  rootMargin: '0px 0px -100px 0px'
});

revealElements.forEach(element => {
  observer.observe(element);
});

// Reveal elements immediately if they're already in view on page load
window.addEventListener('load', () => {
  revealElements.forEach(element => {
    const rect = element.getBoundingClientRect();
    if (rect.top < window.innerHeight) {
      element.classList.add('visible');
    }
  });
});
