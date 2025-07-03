'use client';

import Image from "next/image";
import { useRef, useState } from "react";

export default function Page() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [language, setLanguage] = useState("English");
  const [tone, setTone] = useState("neutral");
  const [feature, setFeature] = useState("summary");
  const [resultPath, setResultPath] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    setLoading(true);
    setError(null);
    setResultPath(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("language", language);
    formData.append("tone", tone);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/${feature}/`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Server responded with ${res.status}`);
      }

      const data = await res.json();
      const path =
        data.summary_path || data.srt_path || data.txt_path || data.path;

      if (!path) {
        throw new Error("No downloadable file path received.");
      }

      setResultPath(path);
    } catch (err) {
      if (err instanceof Error) {
        console.error("Upload failed:", err.message);
        setError(err.message);
      } else {
        console.error("Upload failed:", err);
        setError("An unknown error occurred");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!resultPath) return;
    const a = document.createElement("a");
    a.href = `${process.env.NEXT_PUBLIC_API_BASE}/${resultPath}`;
    a.download = resultPath.split("/").pop() || "downloaded_file";
    a.click();
  };

  return (
    <div className="grid grid-rows-[auto_1fr_auto] items-center justify-items-center min-h-screen p-8 gap-12 sm:p-20 font-sans">
      <main className="flex flex-col gap-8 items-center sm:items-start w-full max-w-2xl">
        <Image
          src="/next.svg?v=2"
          alt="Next.js logo"
          width={180}
          height={38}
        />

        <div className="w-full">
          <h1 className="text-2xl font-bold mb-4">Upload Audio/Video</h1>

          {/* Feature Selector */}
          <label className="block text-sm font-medium mb-1">Feature</label>
          <select
            value={feature}
            onChange={(e) => setFeature(e.target.value)}
            className="border px-3 py-2 rounded w-full mb-4"
          >
            <option value="summary">Summary</option>
            <option value="subtitles">Subtitles</option>
            <option value="slides">Slides</option>
            <option value="poster">Poster</option>
          </select>

          {/* Language and Tone */}
          <div className="flex gap-4 mb-4">
            <div className="flex-1">
              <label className="block text-sm font-medium mb-1">Language</label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="border px-3 py-2 rounded w-full"
              >
                <option value="English">English</option>
                <option value="Chinese">Chinese</option>
                <option value="French">French</option>
                <option value="Spanish">Spanish</option>
                <option value="German">German</option>
              </select>
            </div>

            <div className="flex-1">
              <label className="block text-sm font-medium mb-1">Tone</label>
              <select
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                className="border px-3 py-2 rounded w-full"
              >
                <option value="neutral">Neutral</option>
                <option value="formal">Formal</option>
                <option value="informal">Informal</option>
                <option value="academic">Academic</option>
                <option value="friendly">Friendly</option>
              </select>
            </div>
          </div>

          {/* File Picker */}
          <div className="flex gap-4 mb-4">
            <button
              type="button"
              onClick={() => inputRef.current?.click()}
              className="bg-gray-300 text-black px-4 py-2 rounded hover:bg-gray-400"
            >
              Choose File
            </button>
            <input
              ref={inputRef}
              type="file"
              accept="audio/*,video/*"
              style={{ display: "none" }}
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
            <button
              onClick={handleUpload}
              disabled={loading}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? "Processing..." : "Upload"}
            </button>
          </div>

          <p className="text-sm mb-2">
            Selected file: <span className="font-semibold">{file?.name || "None"}</span>
          </p>

          {error && <p className="text-red-600 mt-2">{error}</p>}

          {resultPath && (
            <div className="mt-6 bg-green-100 p-4 rounded flex flex-col gap-2">
              <p className="text-green-800">Your file is ready:</p>
              <button
                onClick={handleDownload}
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
              >
                Download Result
              </button>
            </div>
          )}
        </div>
      </main>

      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center text-sm">
        <a href="https://nextjs.org/learn" target="_blank" rel="noopener noreferrer" className="hover:underline">
          Learn
        </a>
        <a href="https://vercel.com/templates?framework=next.js" target="_blank" rel="noopener noreferrer" className="hover:underline">
          Examples
        </a>
        <a href="https://nextjs.org" target="_blank" rel="noopener noreferrer" className="hover:underline">
          Go to nextjs.org →
        </a>
      </footer>
    </div>
  );
}
