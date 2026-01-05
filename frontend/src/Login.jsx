import React, { useState } from 'react'
import axios from 'axios'

export function Login(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [token, setToken] = useState(localStorage.getItem('token') || '')

  async function handleLogin(e){
    e.preventDefault()
    try{
      const res = await axios.post('/api/auth/token', { username: email, password })
      localStorage.setItem('token', res.data.access_token)
      setToken(res.data.access_token)
      alert('Logged in')
    }catch(err){
      alert('Login failed')
    }
  }

  return (
    <form onSubmit={handleLogin}>
      <input value={email} onChange={(e)=>setEmail(e.target.value)} placeholder="email" />
      <input value={password} onChange={(e)=>setPassword(e.target.value)} type="password" placeholder="password" />
      <button type="submit">Login</button>
    </form>
  )
}
