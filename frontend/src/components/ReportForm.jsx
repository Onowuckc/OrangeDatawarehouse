import React, { useState } from 'react'
import axios from 'axios'

export function ReportForm(){
  const [department, setDepartment] = useState('FIN')
  const [file, setFile] = useState(null)
  const [message, setMessage] = useState('')

  async function submit(e){
    e.preventDefault()
    if(!file){
      setMessage('Please select a CSV or XLSX file to upload')
      return
    }

    try{
      const token = localStorage.getItem('token')
      const headers = token ? { Authorization: `Bearer ${token}` } : {}
      const fd = new FormData()
      fd.append('department_code', department)
      fd.append('file', file)

      const res = await axios.post('/api/reports/submit-file', fd, { headers })
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
      <h3>Submit Report (CSV/XLSX)</h3>
      <div>
        <label>Department code</label>
        <input value={department} onChange={(e)=>setDepartment(e.target.value)} />
      </div>
      <div>
        <label>File</label>
        <input type="file" accept=".csv,.xlsx,.xls" onChange={(e)=>setFile(e.target.files[0])} />
      </div>
      <button type="submit">Upload</button>
      <div>{message}</div>
    </form>
  )
}
