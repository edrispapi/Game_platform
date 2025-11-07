# Vibe Coding AI Frontend Template

This template contains the React and Tailwind CSS source files referenced in the project brief. Copy the `src` directory into a fresh Vite React workspace to bootstrap the Vibe Coding AI experience with the red-dark theme, creator dashboard, and authentication flows.

## Usage

1. Create a new Vite React project (JavaScript) and install dependencies:

```bash
npm create vite@latest vibecoding -- --template react
cd vibecoding
npm install
npm install react-router-dom react-icons tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

2. Replace the generated `src` directory and `tailwind.config.js` with the versions in this template.
3. Update `index.css` imports if necessary and ensure the root `index.html` references `<div id="root"></div>`.
4. Run the development server with `npm run dev`.

The components are designed to integrate with your FastAPI backend once API endpoints are available.
