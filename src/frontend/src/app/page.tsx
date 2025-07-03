'use client';

import Image from "next/image";
import { useRef, useState } from "react";

export default function Page() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<{ transcript?: string; summary?: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/upload/`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Server responded with ${res.status}`);
      }

      const data = await res.json();
      setResult(data);
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

  return (
    <div className="grid grid-rows-[auto_1fr_auto] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-sans">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start w-full max-w-2xl">
        <Image
          src="/next.svg?v=2"
          alt="Next.js logo"
          width={180}
          height={38}
        />

        <div className="w-full">
          <h1 className="text-2xl font-bold mb-4">Upload Audio/Video</h1>

          {/* File picker */}
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
              onChange={(e) => {
                const selected = e.target.files?.[0] || null;
                setFile(selected);
                console.log("Chosen file:", selected);
              }}
            />

            <button
              onClick={handleUpload}
              disabled={loading}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? "Processing..." : "Upload"}
            </button>
          </div>

          {/* File name display */}
          <p className="text-sm mb-2">
            Selected file: <span className="font-semibold">{file?.name || "None"}</span>
          </p>

          {/* Error message */}
          {error && <p className="text-red-600 mt-2">{error}</p>}

          {/* Result */}
          {result?.summary && (
            <div className="mt-6 bg-gray-100 p-4 rounded">
              <h2 className="font-semibold text-lg mb-2">Summary:</h2>
              <p className="text-sm whitespace-pre-wrap">{result.summary}</p>
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
