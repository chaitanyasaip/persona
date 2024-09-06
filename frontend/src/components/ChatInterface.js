import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ref, push, onValue, off } from 'firebase/database';
import { db } from '../firebaseConfig';
import FileUpload from './FileUpload';

function ChatInterface() {
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    /*
    const chatRef = ref(db, 'chats');
    onValue(chatRef, (snapshot) => {
      const data = snapshot.val();
      */
      console.log("Connecting to Firebase...");
      const chatRef = ref(db, 'chats');
      onValue(chatRef, (snapshot) => {
        const data = snapshot.val();
        console.log("Received data from Firebase:", snapshot.val());
      if (data) {
        setChatHistory(Object.values(data));
      }
    });

    return () => {
      off(chatRef);
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    const newMessage = { role: 'user', content: query };

    try {
      // Add user message to Firebase
      await push(ref(db, 'chats'), newMessage);

      const response = await axios.post(`${process.env.REACT_APP_API_URL}/query`, { text: query });
      const aiResponse = { role: 'assistant', content: response.data.answer };
      
      // Add AI response to Firebase
      await push(ref(db, 'chats'), aiResponse);
    } catch (error) {
      console.error('Error querying portfolio:', error);
      const errorMessage = { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' };
      await push(ref(db, 'chats'), errorMessage);
    }

    setIsLoading(false);
    setQuery('');
  };

  return (
    <div className="chat-interface">
      <FileUpload />
      <div className="chat-history">
        {chatHistory.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <p>{message.content}</p>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="chat-input">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about my skills and experience..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Thinking...' : 'Send'}
        </button>
      </form>
    </div>
  );
}

export default ChatInterface;