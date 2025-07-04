import React, { useState } from "react";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [language, setLanguage] = useState("English");
  const [tone, setTone] = useState("neutral");
  const [feature, setFeature] = useState("summary");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const pollStatus = async (taskId) => {
    const base = process.env.NEXT_PUBLIC_API_BASE;
    let attempts = 0;
    const maxAttempts = 300; // ~5 minutes
    const interval = 1000;

    while (attempts < maxAttempts) {
      await new Promise((r) => setTimeout(r, interval));
      const statusRes = await fetch(`${base}/status/${taskId}`);
      const statusData = await statusRes.json();

      if (statusData.status === "done") return statusData;
      if (statusData.status === "error") throw new Error(statusData.message || "Processing failed");
      attempts++;
    }

    throw new Error("Timeout: Task took too long");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResponse(null);

    if (!file) return alert("Please select a file");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("language", language);
    formData.append("tone", tone);

    setLoading(true);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/${feature}/`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error(`Server responded with ${res.status}`);

      const { task_id, status, message } = await res.json();

      if (feature === "summary") {
        const result = await pollStatus(task_id);
        setResponse(result);
      } else {
        // for subtitles/slides/poster which still return result directly
        setResponse({ message, task_id });
      }
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
    <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1rem", maxWidth: 600 }}>
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

      {error && <p style={{ color: "red" }}>{error}</p>}

      {response && (
        <div style={{ marginTop: 20 }}>
          <strong>{response.message || "Processing complete!"}</strong>
          <br />
          {(response.summary_path || response.srt_path || response.txt_path || response.path) && (
            <button onClick={handleDownload} style={{ marginTop: 10 }}>
              Download Result
            </button>
          )}
        </div>
      )}
    </form>
  );
}

export default UploadForm;
