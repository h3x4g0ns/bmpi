import React, { Component } from 'react';

class Sidebar extends Component {
  render() {
    return (
      <div className="bg-gray-800 text-white w-64 h-screen p-4">
        <h1 className="text-2xl font-semibold mb-4">Dashboard</h1>
        <ul>
          <li className="mb-2">Home</li>
          <li className="mb-2">Analytics</li>
          <li className="mb-2">Settings</li>
        </ul>
      </div>
    );
  }
}

class MainContent extends Component {
  render() {
    return (
      <div className="flex-1 p-4">
        <h2 className="text-xl font-semibold mb-4">Welcome to the Dashboard!</h2>
        <p>This is the main content area of your dashboard.</p>
      </div>
    );
  }
}

class App extends Component {
  render() {
    return (
      <div className="flex h-screen">
        <Sidebar />
        <MainContent />
      </div>
    );
  }
}

export default App;
