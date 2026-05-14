import { Link } from 'react-router-dom'

export default function StudentCard({ student, onDelete }) {
  const { id, name, age, email, city = 'Unknown' } = student

  return (
    <div className="sma-student-card">

      {/* Avatar */}
      <div className="sma-student-card-avatar">
        {name?.charAt(0).toUpperCase()}
      </div>

      {/* Body */}
      <div className="sma-student-card-body">
        <h3 className="sma-student-card-name">{name}</h3>

        <p className="sma-student-card-detail">{email}</p>

        <div className="sma-student-card-footer">
          <span className="sma-student-card-age">Age: {age}</span>
          <span className="sma-student-card-tag">{city}</span>
        </div>
      </div>

      {/* Actions */}
      <div className="sma-card-actions">
        <Link to={`/students/${id}/edit`} className="sma-btn-icon">✎</Link>

        <button
          className="sma-btn-icon sma-btn-icon-delete"
          onClick={() => onDelete(id)}
        >
          ✕
        </button>
      </div>
    </div>
  )
}