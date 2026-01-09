import React, { useState } from 'react'
import axios from 'axios'

export function ReportForm(){
  const [department, setDepartment] = useState('FIN')
  const [payload, setPayload] = useState('{"k": "v"}')
  const [message, setMessage] = useState('')

  async function submit(e){
    e.preventDefault()
    let body
    try{
      body = JSON.parse(payload)
    }catch(parseErr){
      setMessage('Payload must be valid JSON: ' + parseErr.message)
      return
    }

    try{
      const token = localStorage.getItem('token')
      const headers = token ? { Authorization: `Bearer ${token}` } : {}
      const res = await axios.post('/api/reports/submit', {
        department_code: department,
        payload: body,
      }, { headers })
      // surface debug info for inspection
      window.__DW_DEBUG__ = Object.assign({}, window.__DW_DEBUG__ || {}, { lastSubmit: res.data })
      setMessage('Submitted: id=' + (res.data?.id ?? '<no id>'))
    }catch(err){
      console.error(err)
      const msg = err?.response?.data || err.message || String(err)
      window.__DW_DEBUG__ = Object.assign({}, window.__DW_DEBUG__ || {}, { lastSubmitError: msg })
      setMessage('Submission failed: ' + msg)
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
