import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const name: string = "初音ミク"
  const classApp = "App"
  return (
    <div className={classApp}>
      <h1>
        {name}かわいい
      </h1>
    </div>
  );
}

export default App;
