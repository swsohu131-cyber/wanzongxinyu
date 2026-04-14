/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 禅意治愈风格配色
        primary: {
          50: '#FAF7F2',
          100: '#F5F0E8',
          200: '#E8E4DD',
          300: '#D4CCC0',
          400: '#B8ADA0',
          500: '#9C8E80',
          600: '#7A6E60',
          700: '#5A5048',
          800: '#4A4543',
          900: '#3A3533',
        },
        accent: {
          green: '#A8C5B5',  // 舒心绿
          orange: '#D4A574', // 柔和橙
        }
      },
      fontFamily: {
        sans: ['"PingFang SC"', '"Microsoft YaHei"', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
