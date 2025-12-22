import React, { useState, useRef, useEffect } from 'react';

// Floating Chatbot Component
const FloatingChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, type: 'bot', content: 'Hello! I\'m your AI assistant for the Physical AI & Humanoid Robotics Textbook. I\'m connected to the RAG system and ready to answer questions about the textbook content. Ask me anything!' }
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
      const response = await fetch('http://localhost:8000/api/v1/query/', {
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
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen ? (
        <div className="bg-white rounded-2xl shadow-xl border border-gray-200 w-80 h-[500px] flex flex-col">
          {/* Chat Header */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white rounded-t-2xl p-4 flex justify-between items-center">
            <div className="flex items-center gap-2">
              <span className="text-xl">📖</span>
              <h3 className="font-bold">Textbook AI</h3>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:bg-white/20 rounded-full p-1 transition-colors"
            >
              ✕
            </button>
          </div>

          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`mb-3 p-3 rounded-lg ${
                  message.type === 'user'
                    ? 'bg-blue-500 text-white ml-auto max-w-[85%] text-right'
                    : 'bg-gray-200 text-gray-800 mr-auto max-w-[85%]'
                }`}
              >
                <div className="font-semibold text-xs mb-1">
                  {message.type === 'user' ? 'You' : 'AI Assistant'}
                </div>
                <div className="text-sm">{message.content}</div>

                {message.sources && message.sources.length > 0 && (
                  <details className="mt-2 text-xs">
                    <summary className="text-blue-600 cursor-pointer font-medium">Show Sources ({message.sources.length})</summary>
                    <div className="mt-2 space-y-2">
                      {message.sources.map((source, idx) => (
                        <div key={idx} className="bg-blue-50 p-3 rounded-lg border border-blue-100">
                          <div className="font-medium text-blue-700 mb-1">Source {idx + 1} (Score: {(source.relevance_score * 100).toFixed(1)}%)</div>
                          {source.section_title && (
                            <div className="text-xs text-gray-600 mb-1"><strong>Section:</strong> {source.section_title}</div>
                          )}
                          {source.page_number && (
                            <div className="text-xs text-gray-600 mb-1"><strong>Page:</strong> {source.page_number}</div>
                          )}
                          <div className="text-sm mt-1">{source.content}</div>
                          {source.citation && (
                            <div className="text-xs text-gray-500 mt-1 italic">{source.citation}</div>
                          )}
                        </div>
                      ))}
                    </div>
                  </details>
                )}
              </div>
            ))}
            {isLoading && (
              <div className="mb-3 p-3 rounded-lg bg-gray-200 text-gray-800 mr-auto max-w-[85%]">
                <div className="font-semibold text-xs mb-1">AI Assistant</div>
                <div className="flex items-center gap-2">
                  <span>Thinking...</span>
                  <span className="animate-pulse">💬</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Chat Input */}
          <div className="p-3 border-t border-gray-200 bg-white">
            <div className="flex gap-2">
              <textarea
                className="flex-1 border border-gray-300 rounded-lg p-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                placeholder="Ask a question..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={isLoading}
                rows={2}
              />
              <button
                className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg p-2 transition-colors disabled:opacity-50"
                onClick={sendMessage}
                disabled={isLoading || !inputValue.trim()}
              >
                <span className="text-lg">➤</span>
              </button>
            </div>
          </div>
        </div>
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white rounded-full w-14 h-14 flex items-center justify-center shadow-lg hover:shadow-xl transition-shadow"
        >
          <span className="text-2xl">📖</span>
        </button>
      )}
    </div>
  );
};

export default FloatingChatbot;