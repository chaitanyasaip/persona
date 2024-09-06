import React, { useState } from 'react';
import axios from 'axios';
import ResponseDisplay from './ResponseDisplay';
import FileUpload from './FileUpload';

function ChatInterface() {
  const [query, setQuery] = useState('');
  //const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);



  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const res = await axios.post(`${process.env.REACT_APP_API_URL}/query`, { text: query });
      const newResponse = res.data.answer;
      setResponse(newResponse);
      setChatHistory([...chatHistory, { query, response: newResponse }]);
    } catch (error) {
      console.error('Error querying portfolio:', error);
      setResponse('An error occurred while processing your request.');
    }
    setIsLoading(false);
    setQuery('');
  };

  return (
    <div className="chat-interface">
      <FileUpload />
      <div className="chat-history">
        {chatHistory.map((chat, index) => (
          <div key={index}>
            <p><strong>You:</strong> {chat.query}</p>
            <p><strong>AI:</strong> {chat.response}</p>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about my skills and experience"
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Processing...' : 'Ask'}
        </button>
      </form>
      <ResponseDisplay response={response} />
    </div>
  );
}

export default ChatInterface;