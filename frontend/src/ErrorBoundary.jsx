import React from 'react'

export class ErrorBoundary extends React.Component {
  constructor(props){
    super(props)
    this.state = { error: null }
  }

  static getDerivedStateFromError(error){
    return { error }
  }

  componentDidCatch(error, info){
    console.error('ErrorBoundary caught', error, info)
  }

  render(){
    if(this.state.error){
      return <div role="alert" style={{padding:20, background:'#fee', border:'1px solid #f99'}}>An error occurred: {String(this.state.error)}</div>
    }
    return this.props.children
  }
}
