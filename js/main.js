// main.js – Core interactivity for Premium Portfolio
// ----------------------------------------------------------
// State management
const state = {
  theme: localStorage.getItem('theme') || 'light', // 'light' or 'dark'
  menuOpen: false,
};

// DOM Elements
const htmlEl = document.documentElement;
const themeToggleBtn = document.getElementById('themeToggle');
const hamburgerBtn = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');
const scrollTopBtn = document.getElementById('scrollTop');
const navbar = document.getElementById('navbar');
const loader = document.getElementById('loader');
const errorMsg = document.getElementById('errorMsg');
const emptyMsg = document.getElementById('emptyMsg');
const projectsContainer = document.getElementById('projectsContainer');
const contactForm = document.getElementById('contactForm');
const formSuccess = document.getElementById('formSuccess');

// ----------------------------------------------------------
// Utility Functions
// ----------------------------------------------------------
const setTheme = (theme) => {
  htmlEl.setAttribute('data-theme', theme);
  state.theme = theme;
  localStorage.setItem('theme', theme);
  themeToggleBtn.textContent = theme === 'dark' ? '☀️' : '🌙';
};

const toggleTheme = () => {
  setTheme(state.theme === 'dark' ? 'light' : 'dark');
};

const toggleMenu = () => {
  state.menuOpen = !state.menuOpen;
  navLinks.classList.toggle('active', state.menuOpen);
  hamburgerBtn.classList.toggle('active', state.menuOpen);
};

const showScrollTop = () => {
  if (window.scrollY > 300) {
    scrollTopBtn.classList.add('show');
  } else {
    scrollTopBtn.classList.remove('show');
  }
};

const handleScrollNavStyle = () => {
  if (window.scrollY > 60) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
};

// ----------------------------------------------------------
// Intersection Observer – reveal animations
// ----------------------------------------------------------
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.2 }
);

document.querySelectorAll('section').forEach((sec) => {
  sec.classList.add('reveal');
  revealObserver.observe(sec);
});

// ----------------------------------------------------------
// GitHub API – fetch repositories
// ----------------------------------------------------------
const GITHUB_USERNAME = 'skandnl'; // <-- replace with your GitHub handle
const REPO_API_URL = `https://api.github.com/users/${GITHUB_USERNAME}/repos?sort=updated`;

const renderProjectCard = (repo) => {
  const card = document.createElement('div');
  card.className = 'project-card';
  card.innerHTML = `
    <h3>${repo.name}</h3>
    <p>${repo.description || 'No description provided.'}</p>
    <a href="${repo.html_url}" target="_blank" rel="noopener">View on GitHub →</a>
  `;
  projectsContainer.appendChild(card);
};

const fetchProjects = async () => {
  loader.style.display = 'block';
  errorMsg.hidden = true;
  emptyMsg.hidden = true;
  try {
    const response = await fetch(REPO_API_URL);
    if (!response.ok) throw new Error('Network response was not ok');
    const repos = await response.json();
    if (!Array.isArray(repos) || repos.length === 0) {
      emptyMsg.hidden = false;
      return;
    }
    // Optional filter – uncomment to hide forks or specific languages
    // const filtered = repos.filter(r => !r.fork);
    const filtered = repos;
    filtered.forEach(renderProjectCard);
  } catch (error) {
    console.error('GitHub fetch error:', error);
    errorMsg.textContent = 'Failed to load projects. Please try again later.';
    errorMsg.hidden = false;
  } finally {
    loader.style.display = 'none';
  }
};

// ----------------------------------------------------------
// Form Validation
// ----------------------------------------------------------
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const showError = (inputEl, message) => {
  const errorEl = document.getElementById(`${inputEl.id}Error`);
  errorEl.textContent = message;
};

const clearError = (inputEl) => {
  const errorEl = document.getElementById(`${inputEl.id}Error`);
  errorEl.textContent = '';
};

const validateForm = () => {
  let valid = true;
  const name = contactForm.name;
  const email = contactForm.email;
  const message = contactForm.message;

  // Name validation
  if (name.value.trim() === '') {
    showError(name, 'Name is required.');
    valid = false;
  } else {
    clearError(name);
  }

  // Email validation
  if (email.value.trim() === '') {
    showError(email, 'Email is required.');
    valid = false;
  } else if (!emailRegex.test(email.value.trim())) {
    showError(email, 'Enter a valid email address.');
    valid = false;
  } else {
    clearError(email);
  }

  // Message validation
  if (message.value.trim() === '') {
    showError(message, 'Message cannot be empty.');
    valid = false;
  } else {
    clearError(message);
  }

  return valid;
};

contactForm.addEventListener('submit', (e) => {
  e.preventDefault();
  if (validateForm()) {
    // In a real app you'd send the data to a server.
    formSuccess.hidden = false;
    contactForm.reset();
    setTimeout(() => (formSuccess.hidden = true), 4000);
  }
});

// ----------------------------------------------------------
// Event Listeners
// ----------------------------------------------------------
themeToggleBtn.addEventListener('click', toggleTheme);
hamburgerBtn.addEventListener('click', toggleMenu);
navLinks.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    // Close menu on mobile after navigation
    if (state.menuOpen) toggleMenu();
  });
});
scrollTopBtn.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});
window.addEventListener('scroll', () => {
  showScrollTop();
  handleScrollNavStyle();
});

// ----------------------------------------------------------
// Initialization
// ----------------------------------------------------------
(() => {
  // Apply persisted theme
  setTheme(state.theme);

  // Set current year in footer
  const yearEl = document.getElementById('currentYear');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Load GitHub projects
  fetchProjects();
})();

// End of main.js
