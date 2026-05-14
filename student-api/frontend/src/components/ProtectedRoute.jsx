import { Navigate } from 'react-router-dom'

export default function ProtectedRoute({ children }) {
  const token = localStorage.getItem('token')

  // No token? Redirect to /login immediately
  // replace — user cannot press Back to return to this route
  if (!token) {
    return <Navigate to="/login" replace />
  }

  // Token exists — render whatever was wrapped inside ProtectedRoute
  return children
}

// How ProtectedRoute is used in App.jsx:
//
// <Route path="/students" element={
//   <ProtectedRoute>
//     <>
//       <Header />
//       <main className="sma-main">
//         <StudentList />
//       </main>
//     </>
//   </ProtectedRoute>
// } />
//
// If no token → Navigate renders → user is at /login
// If token exists → children renders → user sees Header + StudentList