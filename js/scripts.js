// Events dynamic rendering
document.addEventListener('DOMContentLoaded', function() {
  const eventsRoot = document.getElementById('events-root');
  if (!eventsRoot) return;
  fetch('../files/events.json')
    .then(response => response.json())
    .then(events => {
      // Helper to parse event date strings to Date objects for sorting
      function parseEventDate(event) {
        // Normalize and extract month, day, year
        let d = event.date.trim();
        let months = ["january","february","march","april","may","june","july","august","september","october","november","december"];
        let lower = d.toLowerCase();
        let year = (d.match(/\d{4}/) || [])[0];
        let monthIndex = months.findIndex(m => lower.includes(m));
        // If no year, use current or next year if event is earlier in the year
        let now = new Date();
        let defaultYear = now.getFullYear();
        if (!year) {
          if (monthIndex !== -1 && monthIndex < now.getMonth()) defaultYear++;
          year = defaultYear;
        } else {
          year = parseInt(year, 10);
        }
        // Find first day in string (handles 25/26, 15-17, etc)
        let dayMatch = d.match(/\b(\d{1,2})\b/);
        let day = dayMatch ? parseInt(dayMatch[1], 10) : 1;
        // If no month found, put at end
        if (monthIndex === -1) return new Date(year, 11, 31);
        return new Date(year, monthIndex, day);
      }
      events.sort((a, b) => parseEventDate(a) - parseEventDate(b));
      eventsRoot.innerHTML = events.map(event => `
        <article class="event-row">
          <div class="event-date-col">${event.date}</div>
          <div class="event-details-col">
            <div class="event-title">${event.name}</div>
            ${event.place ? `<div class="event-location">${event.place}</div>` : ''}
          </div>
          <div class="event-time-col">
            ${event.time ? `<div class="event-time">${event.time}</div>` : ''}
            ${event.note ? `<div class="event-note">${event.note}</div>` : ''}
          </div>
        </article>
      `).join('');
    })
    .catch(err => {
      eventsRoot.innerHTML = '<p>Could not load events.</p>';
      console.error('Events load error:', err);
    });
});
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
