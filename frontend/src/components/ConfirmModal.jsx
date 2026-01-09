import React from 'react'

export function ConfirmModal({ open, title, message, onCancel, onConfirm }){
  if(!open) return null
  return (
    <div className="modal-backdrop">
      <div className="modal">
        <h3>{title}</h3>
        <p>{message}</p>
        <div style={{display:'flex', gap:8, justifyContent:'flex-end'}}>
          <button onClick={onCancel} className="btn btn-ghost">Cancel</button>
          <button onClick={onConfirm} className="btn btn-danger">Confirm</button>
        </div>
      </div>
    </div>
  )
}