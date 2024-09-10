/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'caribbean-current': 'hsla(184, 40%, 33%, 1)',
                'turquoise': 'hsla(169, 89%, 45%, 1)',
                'keppel': 'hsla(169, 55%, 52%, 1)',
                'prussian-blue': 'hsla(204, 62%, 17%, 1)',
            },
        },
    },
    plugins: [],
}