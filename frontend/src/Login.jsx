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
      const token = res.data?.access_token || res.access_token
      if(token){
        localStorage.setItem('token', token)
        localStorage.setItem('dept', department)
        if(res.data?.dept_id) localStorage.setItem('dept_id', String(res.data.dept_id))
        setToken(token)
        alert('Logged in')
      }else{
        alert('Login failed: no token returned')
      }
    }catch(err){
      const serverData = err?.response?.data
      const detail = serverData && typeof serverData === 'object' ? (serverData.detail || JSON.stringify(serverData)) : (err?.message || String(err))
      console.error('Login error', err)
      window.__DW_DEBUG__ = Object.assign({}, window.__DW_DEBUG__ || {}, { lastLoginError: serverData || err?.message })
      alert('Login failed: ' + detail)
    }
  }

  useEffect(()=>{
    async function load(){
      try{
        const res = await axios.get('/api/departments/')
        if(Array.isArray(res.data) && res.data.length) {
          setDepts(res.data)
          // ensure selected department exists
          if(!res.data.find(d => d.code === department)) setDepartment(res.data[0].code)
        }
      }catch(err){
        console.warn('Failed to fetch departments', err)
      }
    }
    load()
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
