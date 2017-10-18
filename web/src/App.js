import React, { Component } from 'react';
import logo from './spotify_logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Zwotify</h1>
        </header>
        <div className="App-center-block">
          <p className="App-intro">Zwift workout to Spotify playlist</p>
          <img src={logo} className="App-logo" alt="logo" />
          <p className="App-footer">Coming soon</p>
        </div>
      </div>
    );
  }
}

export default App;
