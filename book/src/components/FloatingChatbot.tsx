import React, { useState, useRef, useEffect } from 'react';

// Floating Chatbot Component
const FloatingChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, type: 'bot', content: 'Hello! I\'m your AI assistant for the Physical AI & Humanoid Robotics Textbook. Ask me anything!' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [bookConnected, setBookConnected] = useState(true); // Always connected since it's integrated
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { id: messages.length + 1, type: 'user', content: inputValue };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the backend API with proper headers
      const response = await fetch('https://physical-ai-humanoid-robotics-textbook-production-06f9.up.railway.app/api/v1/query/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add authentication header if needed
          // 'Authorization': 'Bearer YOUR_API_KEY_HERE',
        },
        body: JSON.stringify({
          query: inputValue,
          mode: 'global',
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const botMessage = {
          id: messages.length + 2,
          type: 'bot',
          content: data.response,
          sources: data.sources || []
        };
        setMessages(prev => [...prev, botMessage]);
      } else {
        const errorData = await response.json();
        const errorMessage = {
          id: messages.length + 2,
          type: 'bot',
          content: `Error: ${errorData.detail || 'Failed to get response'}`
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage = {
        id: messages.length + 2,
        type: 'bot',
        content: `Network error: ${error.message}. Please make sure the backend server is running.`
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="floating-chat">
      {isOpen ? (
        <div className="chat-container">
          {/* Chat Header */}
          <div className="chat-header">
            <div className="chat-header-content">
              <div className="chat-header-icon">🤖</div>
              <div>
                <h3 className="chat-header-title">AI Assistant</h3>
                <p className="chat-header-subtitle">Physical AI & Humanoid Robotics Textbook</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="close-button"
              aria-label="Close chat"
            >
              ✕
            </button>
          </div>

          {/* Chat Messages */}
          <div className="chat-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.type === 'user' ? 'user-message' : 'bot-message'}`}
              >
                <div className="message-content">
                  {message.type === 'bot' && (
                    <>
                      <strong className="assistant-label">AI Assistant:</strong>
                      <br />
                    </>
                  )}
                  {message.content}
                </div>

                {message.sources && message.sources.length > 0 && (
                  <details className="sources-container">
                    <summary>
                      📚 Sources ({message.sources.length})
                    </summary>
                    <div>
                      {message.sources.map((source, idx) => (
                        <div key={idx} className="source-item">
                          <div className="font-medium">Source {idx + 1} (Score: {(source.relevance_score * 100).toFixed(1)}%)</div>
                          {source.section_title && (
                            <div className="text-xs"><strong>Section:</strong> {source.section_title}</div>
                          )}
                          {source.page_number && (
                            <div className="text-xs"><strong>Page:</strong> {source.page_number}</div>
                          )}
                          <div className="text-sm mt-1">{source.content}</div>
                          {source.citation && (
                            <div className="text-xs italic">{source.citation}</div>
                          )}
                        </div>
                      ))}
                    </div>
                  </details>
                )}
              </div>
            ))}
            {isLoading && (
              <div className="typing-indicator">
                <div className="typing-dots">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Chat Input */}
          <div className="chat-input-area">
            <div className="input-container">
              <textarea
                className="chat-input"
                placeholder="Ask question..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={isLoading}
                rows={1}
                aria-label="Type your message"
              />
              <button
                className="send-button"
                onClick={sendMessage}
                disabled={isLoading || !inputValue.trim()}
                aria-label="Send message"
              >
                <span className="text-lg">➤</span>
              </button>
            </div>
          </div>
        </div>
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          className="chat-button"
          aria-label="Open chat"
        >
          <span>🤖</span>
        </button>
      )}
    </div>
  );
};

export default FloatingChatbot;