# Premium Portfolio Website

## 🎯 Project Overview
A fully responsive, premium‑look portfolio website built **only with HTML, CSS, and vanilla JavaScript**. It showcases:
- Hero, About, Skills, Projects, Contact, and Footer sections
- Dark‑mode toggle with state persisted in `localStorage`
- Mobile‑first responsive layout (breakpoints at 768px & 1024px)
- Hamburger menu for mobile navigation
- Smooth scroll, scroll‑to‑top button, and scroll‑based reveal animations (IntersectionObserver)
- Real‑time GitHub API integration – your public repositories are rendered as project cards with loading/error/empty states
- Client‑side form validation with helpful error messages
- Premium UI: glass‑morphism hero background, micro‑animations, subtle hover effects, and a curated color palette

The site is ready to be deployed on **GitHub Pages**, providing a live URL that can be shared with recruiters or peers.

---
## 🛠️ Tech Stack
- **HTML5** – semantic markup (`<header>`, `<nav>`, `<section>`, `<footer>` etc.)
- **CSS3** – variables, Flexbox, CSS Grid, custom properties, media queries, `backdrop-filter`
- **JavaScript (ES6+)** – modules, `const/let`, arrow functions, `fetch`/`async‑await`, `IntersectionObserver`
- **Git & GitHub** – version control & static site hosting via GitHub Pages

---
## 🚀 Getting Started Locally
1. **Clone the repository** (if you haven’t already):
   ```bash
   git clone https://github.com/skandnl/codyssey.git
   cd codyssey
   ```
2. **Open the project** in VS Code and launch a live‑server extension (or any static‑file server). The site will be served at `http://127.0.0.1:5500` by default.
3. **Customize** – replace `images/profile.jpg` with your own portrait and edit the text in `index.html` (name, bio, skills, etc.).
4. **Set your GitHub username** – the file `js/main.js` already contains `const GITHUB_USERNAME = 'skandnl';`. If you want to display a different account, change that constant.

---
## 📦 Deploy to GitHub Pages
1. **Push the code** to the `main` branch (see the *Git Setup* section below).
2. Go to **GitHub → Settings → Pages**.
3. Under **Source**, select **`main` branch** and the **`/(root)`** folder.
4. Click **Save**. After a few minutes GitHub will publish the site at:
   
   ```
   https://skandnl.github.io/codyssey/
   ```
5. Verify the live URL in a browser – all interactions (dark mode, project cards, form validation, etc.) should work without console errors.

---
## 🗂️ Project Structure
```
portfolio-website/
├─ index.html          # entry point, semantic sections
├─ css/
│  └─ style.css       # design system, responsive layout
├─ js/
│  └─ main.js         # core interactivity & GitHub API
├─ images/
│  └─ profile.jpg     # (replace with your own)
├─ README.md           # you are reading it!
└─ .gitignore          # ignores OS & editor artefacts
```

---
## ⚙️ Git Setup & Initial Commit
A helper script (`git_setup.sh`) is included to:
```bash
#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
# Initialise repo if needed
if [ ! -d .git ]; then git init; fi
# Stage everything and commit
git add .
git commit -m "Initial commit – premium portfolio website"
# Ensure we are on main
git branch -M main
# Add remote (won’t error if it already exists)
git remote add origin https://github.com/skandnl/codyssey.git || true
# Push
git push -u origin main
```
Run it with:
```bash
chmod +x git_setup.sh
./git_setup.sh
```

---
## 📜 License
Feel free to use this project as a personal portfolio template. If you reuse the code publicly, a simple **MIT License** is recommended.

---
## 🙏 Acknowledgements
- Hero background created with AI‑generated glass‑morphism image.
- Icons & fonts from Google Fonts (Inter) and Font Awesome (optional).

Enjoy building your showcase! 🎉
