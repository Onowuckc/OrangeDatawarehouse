import React, { useEffect, useState } from 'react'
import axios from 'axios'

export function ReportsList(){
  const [reports, setReports] = useState([])

  useEffect(()=>{
    async function load(){
      try{
        const token = localStorage.getItem('token')
        const headers = token ? { Authorization: `Bearer ${token}` } : {}
        const res = await axios.get('/api/reports', { headers })
        // Normalize response: ensure an array. If not, surface debug info so we can inspect payload.
        if(Array.isArray(res.data)){
          setReports(res.data)
        }else{
          console.warn('Unexpected /api/reports response, expected array:', res.data)
          window.__DW_DEBUG__ = Object.assign({}, window.__DW_DEBUG__ || {}, { reportsResponse: res.data })
          setReports([])
          // store an error for the UI
          setError('Unexpected response shape from /api/reports (see Debug info)')
        }
      }catch(err){
        console.error(err)
        setError(err.message || String(err))
      }
    }
    load()
  }, [])

  return (
    <section style={{marginTop:20}}>
      <h3>Reports</h3>
      {reports.length === 0 && <div>No reports</div>}
      <ul>
        {reports.map(r => (
          <li key={r.id}>id: {r.id} dept: {r.department_id} status: {r.status}</li>
        ))}
      </ul>
    </section>
  )
}
