import React from 'react'

export function DebugInfo({children}){
  return (
    <details style={{marginTop:12, fontSize:12}}>
      <summary>Debug info</summary>
      <pre>{JSON.stringify(window.__DW_DEBUG__ || {}, null, 2)}</pre>
      {children}
    </details>
  )
}
