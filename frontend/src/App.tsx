import { DropZone } from "./components/DropZone";
import "./App.css";

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Data Processing App</h1>
        <p>Phase 1 — Drag-and-Drop Proof of Concept</p>
      </header>
      <main className="app-main">
        <DropZone />
      </main>
    </div>
  );
}

export default App;
