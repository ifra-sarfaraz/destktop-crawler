import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [folderPath, setFolderPath] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [ragAnswer, setRagAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("search");

  const crawlFiles = async () => {
    if (!folderPath) return alert("Please enter a folder path.");
    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/crawl", {
        folder_path: folderPath,
      });
      alert(res.data.status);
    } catch (err) {
      console.error(err);
      alert(
        "Error crawling path. Make sure it's correct and backend has permission."
      );
    }
    setLoading(false);
  };

  const search = async () => {
    setLoading(true);
    setRagAnswer("");
    try {
      const res = await axios.post("http://127.0.0.1:8000/search", {
        query,
        use_stemming: false,
        method: "tfidf",
      });
      setResults(res.data.results);
    } catch (err) {
      console.error(err);
      alert("Error performing search. Ensure the backend is running.");
    }
    setLoading(false);
  };

  const askLLM = async () => {
    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/rag", {
        query,
        use_stemming: false,
        method: "tfidf",
      });
      setRagAnswer(res.data.answer);
    } catch (err) {
      console.error(err);
      alert(
        "Error querying LLM. Ensure the backend and OpenAI API key are configured."
      );
    }
    setLoading(false);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="app-title">📂 Local File Search + RAG</h1>
      </header>
      <main className="main-content">
        <section className="section card">
          <h2 className="section-title">1. Crawl a Folder</h2>
          <div className="input-group">
            <input
              type="text"
              className="input"
              placeholder="Enter folder path (e.g., C:\\Users\\You\\Documents)"
              value={folderPath}
              onChange={(e) => setFolderPath(e.target.value)}
            />
            <button onClick={crawlFiles} className="button primary">
              Crawl Folder
            </button>
          </div>
        </section>
        <section className="section card">
          <h2 className="section-title">2. Search or Ask</h2>
          <div className="tab-group">
            <button
              className={`tab ${activeTab === "search" ? "active" : ""}`}
              onClick={() => setActiveTab("search")}
            >
              Search
            </button>
            <button
              className={`tab ${activeTab === "llm" ? "active" : ""}`}
              onClick={() => setActiveTab("llm")}
            >
              Ask LLM 🤖
            </button>
          </div>
          <div className="input-group">
            <input
              type="text"
              className="input"
              placeholder="Enter your query..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            {activeTab === "search" ? (
              <button onClick={search} className="button primary">
                Search
              </button>
            ) : (
              <button onClick={askLLM} className="button secondary">
                Ask LLM
              </button>
            )}
          </div>
        </section>
        {loading && <div className="loading">Loading...</div>}
        {results.length > 0 && (
          <section className="section card results-section">
            <h2 className="section-title">🔎 Search Results</h2>
            <ul className="results-list">
              {results.map((r, i) => (
                <li key={i} className="result-item">
                  <div className="result-path">{r.path}</div>
                  <div className="result-snippet">{r.snippet}</div>
                  <div className="result-meta">
                    <span className="result-score">
                      📈 Score: {r.score.toFixed(3)}
                    </span>
                    {r.query_count !== undefined && (
                      <span className="result-count">
                        🔍 Matches: {r.query_count}
                      </span>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </section>
        )}
        {ragAnswer && (
          <section className="section card answer-section">
            <h2 className="section-title">🧠 LLM Answer</h2>
            <div className="llm-answer">{ragAnswer}</div>
          </section>
        )}
      </main>
      <footer className="app-footer">
        <span>
          Made with <span style={{ color: "#e25555" }}>❤</span> for local file
          intelligence
        </span>
      </footer>
    </div>
  );
}

export default App;
