/** Build: npx tailwindcss@3 -c tailwind.config.js -i css/tailwind.src.css -o css/tailwind.css --minify */
module.exports = {
  content: [
    './index.html',
    './404.html',
    './{about,articles,compare,compatibility,faq,privacy,quiz,search,setups,fish}/**/*.html',
    './{de,es,fr}/**/*.html',
    './{de,es,fr}/js/*.js',
  ],
  theme: {
    extend: {
      fontFamily: { sans: ['Plus Jakarta Sans', 'sans-serif'] },
    },
  },
  plugins: [],
};
