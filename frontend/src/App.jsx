import React, { useState, useRef, useEffect } from 'react';

function App() {
  const [messages, setMessages] = useState([
    { role: 'agent', agent: 'System', content: 'Welcome to the Retail Agentic AI Platform. Ask me anything about inventory, sales, or orders.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => crypto.randomUUID());
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setIsLoading(true);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const res = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg, session_id: sessionId })
      });
      
      const data = await res.json();
      
      if (data.responses) {
        // Map backend format to UI format
        const newMessages = data.responses.map(r => ({
          role: 'agent',
          agent: r.agent,
          content: r.content
        }));
        setMessages(prev => [...prev, ...newMessages]);
      }
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { role: 'agent', agent: 'System', content: err.message }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Retail AI Nexus</h1>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Multi-Agent Orchestrator</div>
      </header>

      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role} ${msg.agent || ''}`}>
            {msg.role === 'agent' && (
              <div className="message-header">{msg.agent} Agent</div>
            )}
            <div dangerouslySetInnerHTML={{__html: msg.content.replace(/\n/g, '<br/>')}} />
          </div>
        ))}
        
        {isLoading && (
          <div className="message agent System">
            <div className="message-header">Processing</div>
            <div className="typing-indicator">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <div className="input-area">
        <form className="input-form" onSubmit={handleSubmit}>
          <input 
            type="text" 
            placeholder="Compare sales vs inventory levels for the top 50 products..." 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
          />
          <button type="submit" disabled={!input.trim() || isLoading}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
