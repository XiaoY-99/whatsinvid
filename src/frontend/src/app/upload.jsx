import React, { useState } from "react";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [language, setLanguage] = useState("English");
  const [tone, setTone] = useState("neutral");
  const [feature, setFeature] = useState("summary");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResponse(null);

    if (!file) return alert("Please select a file");

    setLoading(true); // Moved up

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("language", language);
      formData.append("tone", tone);

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/${feature}/`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Server responded with ${res.status}`);
      }

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setError(err.message || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!response) return;

    const filePath =
      response.summary_path || response.srt_path || response.txt_path || response.path;

    if (!filePath) return alert("No downloadable file path found.");

    const fileName = filePath.split("/").pop();
    const link = document.createElement("a");
    link.href = `${process.env.NEXT_PUBLIC_API_BASE}/download/${fileName}?download=true`;
    link.setAttribute("download", "");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{ display: "flex", flexDirection: "column", gap: "1rem", maxWidth: 600 }}
    >
      <input type="file" accept="audio/*,video/*" onChange={(e) => setFile(e.target.files[0])} />

      <label>Feature:</label>
      <select value={feature} onChange={(e) => setFeature(e.target.value)}>
        <option value="summary">Summary</option>
        <option value="subtitles">Subtitles</option>
        <option value="slides">Slides</option>
        <option value="poster">Poster</option>
      </select>

      <label>Language:</label>
      <select value={language} onChange={(e) => setLanguage(e.target.value)}>
        <option value="English">English</option>
        <option value="Chinese">Chinese</option>
        <option value="French">French</option>
        <option value="German">German</option>
        <option value="Spanish">Spanish</option>
      </select>

      <label>Tone:</label>
      <select value={tone} onChange={(e) => setTone(e.target.value)}>
        <option value="neutral">Neutral</option>
        <option value="scientific">Scientific</option>
        <option value="business">Business</option>
        <option value="marketing">Marketing</option>
        <option value="friendly">Friendly</option>
      </select>

      <button type="submit" disabled={loading}>
        {loading ? "Uploading..." : "Upload"}
      </button>
      
      {loading && (
        <div style={{ 
          marginTop: "1rem", 
          display: "flex", 
          alignItems: "center", 
          gap: "0.5rem", 
          fontSize: "0.9rem", 
          color: "#555" 
        }}>
          <span>It may take some time...</span>
          <svg
            style={{ animation: "spin 1s linear infinite", width: "16px", height: "16px" }}
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              fill="currentColor"
              d="M4 12a8 8 0 018-8v4l3.5-3.5L12 0v4a8 8 0 00-8 8z"
            />
          </svg>
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}

      {response && (
        <div style={{ marginTop: 20 }}>
          <strong>{response.message}</strong>
          <br />
          {(response.summary_path || response.srt_path || response.txt_path || response.path) && (
            <button onClick={handleDownload} style={{ marginTop: 10 }}>
              Download Result
            </button>
          )}
        </div>
      )}

      {/* Spinner CSS */}
      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </form>
  );
}

export default UploadForm;
