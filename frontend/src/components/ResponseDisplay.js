import React from 'react';

function ResponseDisplay({ response }) {
  return (
    <div className="response-display">
      <h2>Response:</h2>
      <p>{response}</p>
    </div>
  );
}

export default ResponseDisplay;