import React, { useState } from "react";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [language, setLanguage] = useState("English");
  const [tone, setTone] = useState("neutral");
  const [response, setResponse] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please select a file");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("language", language);
    formData.append("tone", tone);

    const res = await fetch("https://whatsinvid.onrender.com/summary/", {
      method: "POST",
      body: formData,
    });    

    const data = await res.json();
    setResponse(data);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" accept="audio/*,video/*" onChange={(e) => setFile(e.target.files[0])} />

      <label>Language:</label>
      <select value={language} onChange={(e) => setLanguage(e.target.value)}>
        <option>English</option>
        <option>Chinese</option>
        <option>French</option>
        <option>German</option>
      </select>

      <label>Tone:</label>
      <select value={tone} onChange={(e) => setTone(e.target.value)}>
        <option value="neutral">Neutral</option>
        <option value="scientific">Scientific</option>
        <option value="business">Business</option>
        <option value="marketing">Marketing</option>
      </select>

      <button type="submit">Upload & Summarize</button>

      {response && (
        <div style={{ marginTop: 20 }}>
          <strong>{response.message}</strong>
          <p>{response.summary_path && `Summary File: ${response.summary_path}`}</p>
        </div>
      )}
    </form>
  );
}

export default UploadForm;
