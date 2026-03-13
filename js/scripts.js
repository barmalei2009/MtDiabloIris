// Scroll reveal
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

// Nav scroll effect
window.addEventListener('scroll', () => {
  const nav = document.querySelector('nav');
  if (!nav) return;

  if (window.scrollY > 50) {
    nav.style.boxShadow = '0 2px 30px rgba(59,31,94,0.08)';
  } else {
    nav.style.boxShadow = 'none';
  }
});
