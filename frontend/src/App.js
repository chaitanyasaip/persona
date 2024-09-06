import React from 'react';
import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  return (
    <div className="App">
      <aside className="sidebar">
        <div className="logo">Logo</div>
        <nav>
          <ul className="nav-links">
            <li><a href="#discover">discover</a></li>
            <li><a href="#projects">projects</a></li>
            <li><a href="#inbox">inbox</a></li>
            <li><a href="#history">history</a></li>
          </ul>
        </nav>
        <div className="user-profile">
          <img src="path_to_user_image.jpg" alt="User" />
          <span>Sai Chaitanya Pachipulusu</span>
        </div>
      </aside>
      <main className="main-content">
        <h1>find and<br />be found.</h1>
        <ChatInterface />
      </main>
    </div>
  );
}

export default App;
