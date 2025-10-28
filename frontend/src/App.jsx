import { useState, useEffect, useRef } from 'react'
import Vapi from '@vapi-ai/web'
import './App.css'

function App() {
  const [isCallActive, setIsCallActive] = useState(false)
  const [isConnecting, setIsConnecting] = useState(false)
  const [statusMessage, setStatusMessage] = useState('Pronto per iniziare')
  const [transcript, setTranscript] = useState([])
  const vapiRef = useRef(null)

  // Inizializza Vapi
  useEffect(() => {
    const publicKey = import.meta.env.VITE_VAPI_PUBLIC_KEY

    if (!publicKey || publicKey === 'your_vapi_public_key_here') {
      setStatusMessage('⚠️ Configura VITE_VAPI_PUBLIC_KEY in .env')
      return
    }

    vapiRef.current = new Vapi(publicKey)

    // Event listeners
    vapiRef.current.on('call-start', () => {
      console.log('Call started')
      setIsCallActive(true)
      setIsConnecting(false)
      setStatusMessage('Chiamata in corso')
      setTranscript([{ role: 'system', text: 'Chiamata iniziata...' }])
    })

    vapiRef.current.on('call-end', () => {
      console.log('Call ended')
      setIsCallActive(false)
      setIsConnecting(false)
      setStatusMessage('Chiamata terminata')
      setTranscript(prev => [...prev, { role: 'system', text: 'Chiamata terminata.' }])
    })

    vapiRef.current.on('speech-start', () => {
      console.log('Speech started')
      setStatusMessage('Ascolto in corso...')
    })

    vapiRef.current.on('speech-end', () => {
      console.log('Speech ended')
      setStatusMessage('Elaborazione...')
    })

    vapiRef.current.on('message', (message) => {
      console.log('Message:', message)

      // Transcript handling
      if (message.type === 'transcript' && message.transcriptType === 'final') {
        const role = message.role
        const text = message.transcript

        setTranscript(prev => [...prev, { role, text }])
      }

      // Function calls
      if (message.type === 'function-call') {
        console.log('Function called:', message.functionCall)
      }
    })

    vapiRef.current.on('error', (error) => {
      console.error('Vapi error:', error)
      setStatusMessage(`Errore: ${error.message}`)
      setIsCallActive(false)
      setIsConnecting(false)
    })

    return () => {
      if (vapiRef.current) {
        vapiRef.current.stop()
      }
    }
  }, [])

  const startCall = async () => {
    const assistantId = import.meta.env.VITE_ASSISTANT_ID

    if (!assistantId) {
      alert('VITE_ASSISTANT_ID non configurato!')
      return
    }

    setIsConnecting(true)
    setStatusMessage('Connessione in corso...')

    try {
      await vapiRef.current.start(assistantId)
    } catch (error) {
      console.error('Error starting call:', error)
      setStatusMessage('Errore durante la chiamata')
      setIsConnecting(false)
    }
  }

  const endCall = () => {
    if (vapiRef.current) {
      vapiRef.current.stop()
    }
  }

  return (
    <div className="app">
      <div className="container">
        {/* Header */}
        <header className="header">
          <div className="logo">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="40" height="40" rx="8" fill="#2563eb"/>
              <path d="M20 10L28 15V25L20 30L12 25V15L20 10Z" stroke="white" strokeWidth="2" strokeLinejoin="round"/>
              <circle cx="20" cy="20" r="3" fill="white"/>
            </svg>
            <div>
              <h1>Comune di Codroipo</h1>
              <p>Assistente Vocale AI</p>
            </div>
          </div>
        </header>

        {/* Main Card */}
        <main className="main">
          <div className="card">
            <div className="card-header">
              <h2>Demo Assistente Vocale</h2>
              <p>Prova l'assistente AI per i servizi comunali</p>
            </div>

            <div className="card-body">
              {/* Status Indicator */}
              <div className={`status-container ${isCallActive ? 'calling' : isConnecting ? 'active' : ''}`}>
                <div className={`status-indicator ${isCallActive ? 'calling' : isConnecting ? 'active' : ''}`}>
                  <div className="pulse"></div>
                </div>
                <div className="status-text">
                  <h3>{isCallActive ? 'In chiamata' : isConnecting ? 'Connessione...' : 'Pronto'}</h3>
                  <p>{statusMessage}</p>
                </div>
              </div>

              {/* Controls */}
              <div className="controls">
                <button
                  className="btn btn-primary"
                  onClick={startCall}
                  disabled={isCallActive || isConnecting}
                >
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M15.05 5A5 5 0 0 1 19 8.95M15.05 1A9 9 0 0 1 23 8.94m-1 7.98v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                  </svg>
                  Inizia Chiamata
                </button>
                <button
                  className="btn btn-danger"
                  onClick={endCall}
                  disabled={!isCallActive}
                >
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M10.68 13.31a16 16 0 0 0 3.41 2.6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7 2 2 0 0 1 1.72 2v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.42 19.42 0 0 1-3.33-2.67m-2.67-3.34a19.79 19.79 0 0 1-3.07-8.63A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91"></path>
                    <line x1="1" y1="1" x2="23" y2="23"></line>
                  </svg>
                  Termina Chiamata
                </button>
              </div>

              {/* Transcript */}
              <div className="transcript-container">
                <h4>Trascrizione</h4>
                <div className="transcript">
                  {transcript.length === 0 ? (
                    <p className="transcript-empty">La conversazione apparirà qui...</p>
                  ) : (
                    transcript.map((msg, idx) => (
                      <div key={idx} className="transcript-message">
                        <div className={`transcript-role ${msg.role}`}>
                          {msg.role === 'user' ? 'Tu' : msg.role === 'assistant' ? 'Assistente' : 'Sistema'}
                        </div>
                        <div className="transcript-text">{msg.text}</div>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* Info Section */}
              <div className="info-section">
                <h4>💡 Cosa puoi chiedere:</h4>
                <ul>
                  <li>Informazioni su servizi comunali (carta d'identità, certificati, TARI)</li>
                  <li>Prenotazione appuntamenti</li>
                  <li>Orari di apertura uffici</li>
                  <li>Documenti necessari per pratiche</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Tech Info Card */}
          <div className="card tech-card">
            <div className="card-body">
              <h3>Informazioni Tecniche</h3>
              <div className="tech-info">
                <div className="tech-item">
                  <span className="tech-label">Piattaforma:</span>
                  <span className="tech-value">Vapi.ai</span>
                </div>
                <div className="tech-item">
                  <span className="tech-label">Modello:</span>
                  <span className="tech-value">GPT-4o</span>
                </div>
                <div className="tech-item">
                  <span className="tech-label">Voce:</span>
                  <span className="tech-value">ElevenLabs (Italiano)</span>
                </div>
                <div className="tech-item">
                  <span className="tech-label">Integrazioni:</span>
                  <span className="tech-value">Google Calendar, Email</span>
                </div>
              </div>
            </div>
          </div>
        </main>

        {/* Footer */}
        <footer className="footer">
          <p>Demo Tecnica - Assistente AI Comune di Codroipo</p>
          <p>Sviluppato per test tecnico Fullstack Developer AI & Automation</p>
        </footer>
      </div>
    </div>
  )
}

export default App
