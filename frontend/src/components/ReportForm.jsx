import React, { useState } from 'react'
import axios from 'axios'

export function ReportForm(){
  const [department, setDepartment] = useState('FIN')
  const [payload, setPayload] = useState('{"k": "v"}')
  const [message, setMessage] = useState('')

  async function submit(e){
    e.preventDefault()
    try{
      const token = localStorage.getItem('token')
      const headers = token ? { Authorization: `Bearer ${token}` } : {}
      const res = await axios.post('/api/reports/submit', {
        department_code: department,
        payload: JSON.parse(payload),
      }, { headers })
      setMessage('Submitted: id=' + res.data.id)
    }catch(err){
      console.error(err)
      setMessage('Submission failed')
    }
  }

  return (
    <form onSubmit={submit} style={{marginTop:20}}>
      <h3>Submit Report</h3>
      <div>
        <label>Department code</label>
        <input value={department} onChange={(e)=>setDepartment(e.target.value)} />
      </div>
      <div>
        <label>Payload (JSON)</label>
        <textarea value={payload} onChange={(e)=>setPayload(e.target.value)} rows={6} cols={60} />
      </div>
      <button type="submit">Submit</button>
      <div>{message}</div>
    </form>
  )
}
