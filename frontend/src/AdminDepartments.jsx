import React, { useEffect, useState } from 'react'
import axios from 'axios'

export function AdminDepartments(){
  const [depts, setDepts] = useState([])
  const [code, setCode] = useState('')
  const [name, setName] = useState('')
  const [msg, setMsg] = useState('')

  const [confirmOpen, setConfirmOpen] = useState(false)
  const [pending, setPending] = useState(null) // { id, code, timeoutId }

  async function load(){
    const res = await axios.get('/api/departments/')
    setDepts(res.data)
  }

  useEffect(()=>{load()}, [])

  async function create(e){
    e.preventDefault()
    try{
      const token = localStorage.getItem('token')
      const res = await axios.post('/api/departments/', { code, name }, { headers: { Authorization: `Bearer ${token}` } })
      setMsg('Created ' + res.data.code)
      setCode(''); setName('')
      await load()
    }catch(err){
      setMsg('Create failed: ' + (err?.response?.data || err?.message || String(err)))
    }
  }

  function openConfirm(id, code){
    setConfirmOpen(true)
    setPending({ id, code })
  }

  async function confirmDelete(){
    if(!pending) return
    try{
      const token = localStorage.getItem('token')
      await axios.delete(`/api/departments/${pending.id}`, { headers: { Authorization: `Bearer ${token}` } })
      // show undo snackbar
      const timeoutId = setTimeout(()=>{ setPending(null); load() }, 10000) // 10s grace
      setPending({ ...pending, timeoutId })
      setConfirmOpen(false)
      setMsg('Deleted ' + pending.code + ' (undo available)')
    }catch(err){
      setMsg('Delete failed: ' + (err?.response?.data || err?.message || String(err)))
    }
  }

  async function undoDelete(){
    if(!pending) return
    try{
      const token = localStorage.getItem('token')
      await axios.post(`/api/departments/${pending.id}/restore`, {}, { headers: { Authorization: `Bearer ${token}` } })
      clearTimeout(pending.timeoutId)
      setMsg('Restored ' + pending.code)
      setPending(null)
      await load()
    }catch(err){
      setMsg('Restore failed: ' + (err?.response?.data || err?.message || String(err)))
    }
  }

  return (
    <section style={{marginTop:20}}>
      <h3>Admin: Departments</h3>
      <form onSubmit={create} style={{marginBottom:12}}>
        <input placeholder="code" value={code} onChange={(e)=>setCode(e.target.value)} />
        <input placeholder="name" value={name} onChange={(e)=>setName(e.target.value)} />
        <button type="submit">Create</button>
      </form>
      {msg && <div className="msg">{msg}</div>}

      {pending && !pending.timeoutId && (
        <div className="undo">Deleted {pending.code}. <button onClick={undoDelete}>Undo</button></div>
      )}

      {pending && pending.timeoutId && (
        <div className="undo">Deleted {pending.code}. Undo available for 10s. <button onClick={undoDelete}>Undo</button></div>
      )}

      <ul className="dept-list">
        {depts.filter(d=>!d.deleted).map(d => (
          <li key={d.id}>{d.code} - {d.name} <button onClick={()=>openConfirm(d.id, d.code)}>Delete</button></li>
        ))}
      </ul>

      <ConfirmModal open={confirmOpen} title={`Delete ${pending?.code}?`} message={`Are you sure you want to delete ${pending?.code}? This can be undone within 10s.`} onCancel={()=>setConfirmOpen(false)} onConfirm={confirmDelete} />
    </section>
  )
}