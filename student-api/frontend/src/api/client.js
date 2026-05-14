import axios from 'axios'

const client = axios.create({
  // import.meta.env is Vite's way to read env variables
  // VITE_API_URL is set in .env
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export default client

// In development (.env has VITE_API_URL=http://localhost:8000):
//   Every request goes to http://localhost:8000/students

// In production (.env on Vercel has VITE_API_URL=https://your-app.onrender.com):
//   Every request goes to https://your-app.onrender.com/students

// No code changes needed — just swap the .env variable