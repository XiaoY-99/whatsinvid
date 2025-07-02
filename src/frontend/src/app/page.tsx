'use client';

import Image from "next/image";
import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<{ transcript: string; summary: string } | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/upload/`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      console.error("Upload failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-rows-[auto_1fr_auto] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-sans">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start w-full max-w-2xl">
        <Image
          className="dark:invert"
          src="/next.svg"
          alt="Next.js logo"
          width={180}
          height={38}
          priority
        />

        <div className="w-full">
          <h1 className="text-2xl font-bold mb-4">Upload Audio/Video</h1>
          <input
            type="file"
            accept="audio/*,video/*"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="mb-4 block w-full"
          />
          <button
            onClick={handleUpload}
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Processing..." : "Upload"}
          </button>

          {result && (
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
