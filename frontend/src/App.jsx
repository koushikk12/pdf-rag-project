import { useState } from "react";
import { uploadPDF, processPDF, askQuestion } from "./services/api";

function App() {
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState("");
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    try {
      setLoading(true);
      const res = await uploadPDF(file);
      setFilename(res.data.filename);
      alert("Upload successful!");
    } catch {
      alert("Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleProcess = async () => {
    if (!filename) return;

    try {
      setLoading(true);
      await processPDF(filename);
      alert("Document processed!");
    } catch {
      alert("Processing failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async () => {
    if (!query) return;

    const userMsg = { role: "user", text: query };
    setMessages((prev) => [...prev, userMsg]);

    try {
      setLoading(true);
      const res = await askQuestion(query);

      const botMsg = {
        role: "assistant",
        text: res.data.answer,
        sources: res.data.sources
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch {
      alert("Error getting answer.");
    } finally {
      setLoading(false);
      setQuery("");
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>📄 PDF RAG Assistant</h1>

      <div style={{ marginBottom: "20px" }}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload} disabled={loading}>
          Upload
        </button>
        <button onClick={handleProcess} disabled={!filename || loading}>
          Process
        </button>
      </div>

      <div style={{
        border: "1px solid #ccc",
        height: "300px",
        overflowY: "auto",
        padding: "10px",
        marginBottom: "10px"
      }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ marginBottom: "10px" }}>
            <strong>{msg.role === "user" ? "You" : "AI"}:</strong>
            <div>{msg.text}</div>
            {msg.sources && (
              <div style={{ fontSize: "12px", color: "gray" }}>
                Sources: {msg.sources.map((s, i) => (
                  <span key={i}>Page {s.page} </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question..."
        style={{ width: "70%" }}
      />
      <button onClick={handleAsk} disabled={loading}>
        Send
      </button>
    </div>
  );
}

export default App;
