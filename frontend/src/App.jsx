import React from 'react'
import { Login } from './Login'
import { ReportForm } from './components/ReportForm'
import { ReportsList } from './components/ReportsList'

export default function App(){
  return (
    <main>
      <h1>Internal Data Warehouse</h1>
      <Login />
      <ReportForm />
      <ReportsList />
    </main>
  )
}
