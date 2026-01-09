import React from 'react'
import { Login } from './Login'
import { ReportForm } from './components/ReportForm'
import { ReportsList } from './components/ReportsList'
import logo from './logo.svg'
import { DebugInfo } from './DebugInfo'
import { AdminDepartments } from './AdminDepartments'

export default function App(){
  return (
    <main className="container">
      <header>
        <img src={logo} alt="DW logo" />
        <h1>Internal Data Warehouse</h1>
      </header>
      <Login />
      <ReportForm />
      <ReportsList />
      <DebugInfo />
      { (localStorage.getItem('role') || '').includes('GeneralManager') && <AdminDepartments /> }
    </main>
  )
}
