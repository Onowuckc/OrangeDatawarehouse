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
        setReports(res.data)
      }catch(err){
        console.error(err)
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
