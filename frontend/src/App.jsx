import React from 'react'
import { Login } from './Login'
import { ReportForm } from './components/ReportForm'
import { ReportsList } from './components/ReportsList'
import logo from './logo.svg'
import { DebugInfo } from './DebugInfo'
import { AdminDepartments } from './AdminDepartments'

export default function App(){
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role') || ''

  return (
    <main className="container">
      <header>
        <img src={logo} alt="DW logo" />
        <h1>Internal Data Warehouse</h1>
      </header>

      <Login />

      {!token ? (
        <div style={{marginTop:20}}>Please login to submit or view reports.</div>
      ) : (
        <>
          <ReportForm />
          <ReportsList />
          <DebugInfo />
          { role.includes('GeneralManager') && <AdminDepartments /> }
        </>
      )}

    </main>
  )
}
