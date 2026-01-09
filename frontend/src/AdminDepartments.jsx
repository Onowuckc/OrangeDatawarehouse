import React, { useEffect, useState } from 'react'
import axios from 'axios'

export function AdminDepartments(){
  const [depts, setDepts] = useState([])
  const [code, setCode] = useState('')
  const [name, setName] = useState('')
  const [msg, setMsg] = useState('')

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

  async function del(id, code){
    if(!window.confirm(`Delete department ${code}? This action cannot be undone.`)) return
    try{
      const token = localStorage.getItem('token')
      await axios.delete(`/api/departments/${id}`, { headers: { Authorization: `Bearer ${token}` } })
      setMsg('Deleted ' + code)
      await load()
    }catch(err){
      setMsg('Delete failed: ' + (err?.response?.data || err?.message || String(err)))
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
      {msg && <div>{msg}</div>}
      <ul>
        {depts.map(d => (
          <li key={d.id}>{d.code} - {d.name} <button onClick={()=>del(d.id, d.code)}>Delete</button></li>
        ))}
      </ul>
    </section>
  )
}