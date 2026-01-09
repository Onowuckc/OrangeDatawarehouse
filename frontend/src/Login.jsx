import React, { useState, useEffect } from 'react'
import axios from 'axios'

export function Login(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [department, setDepartment] = useState('FIN')
  const [token, setToken] = useState(localStorage.getItem('token') || '')
  const [depts, setDepts] = useState(['FIN','OPS','SAL'])

  async function handleLogin(e){
    e.preventDefault()
    try{
      const res = await axios.post('/api/auth/login', { username: email, password, role: department })
      localStorage.setItem('token', res.access_token || res.data?.access_token)
      localStorage.setItem('dept', department)
      setToken(res.access_token || res.data?.access_token)
      alert('Logged in')
    }catch(err){
      alert('Login failed: ' + (err?.response?.data || err?.message || String(err)))
    }
  }

  useEffect(()=>{
    // Optionally fetch departments from API in the future
  }, [])

  return (
    <form onSubmit={handleLogin} style={{display:'flex', gap:8}}>
      <input value={email} onChange={(e)=>setEmail(e.target.value)} placeholder="email" />
      <input value={password} onChange={(e)=>setPassword(e.target.value)} type="password" placeholder="password" />
      <select value={department} onChange={(e)=>setDepartment(e.target.value)}>
        {depts.map(d => <option key={d} value={d}>{d}</option>)}
      </select>
      <button type="submit">Login</button>
    </form>
  )
}
