import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
)

// BrowserRouter wraps App — every component inside App can now:
// - Use Link to navigate without page reload
// - Call useNavigate() for programmatic navigation
// - Call useParams() to read URL parameters (Day 12)
// - Call useLocation() to read the current URL