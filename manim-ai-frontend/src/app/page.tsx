"use client";

import { useState } from "react";

export default function HomePage() {
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState("");
  const [code, setCode] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setVideoUrl("");
    setCode("");
    setError("");

    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Something went wrong");
      }

      const { videoUrl, generatedCode } = await response.json();
      setVideoUrl(videoUrl);
      setCode(generatedCode);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-12 bg-gray-900 text-white">
      <h1 className="text-5xl font-bold mb-4">Manim AI Animator</h1>
      <p className="text-lg text-gray-400 mb-8">
        Describe the animation you want to see, and let AI bring it to life.
      </p>

      <form onSubmit={handleSubmit} className="w-full max-w-2xl">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="e.g., A blue circle transforming into a red square"
          className="w-full h-24 p-4 text-black bg-gray-200 rounded-md shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="w-full mt-4 py-3 px-4 bg-blue-600 rounded-md text-white font-semibold hover:bg-blue-700 disabled:bg-gray-500"
          disabled={isLoading}
        >
          {isLoading ? "Generating..." : "Generate Animation"}
        </button>
      </form>

      {isLoading && (
        <div className="mt-8">
          <p className="text-lg">⚙️ Rendering video, please wait...</p>
        </div>
      )}

      {error && (
        <div className="mt-8 p-4 bg-red-900 border border-red-500 rounded-md w-full max-w-2xl">
          <p className="font-bold">Error:</p>
          <pre className="whitespace-pre-wrap">{error}</pre>
        </div>
      )}

      {videoUrl && (
        <div className="mt-8 w-full max-w-2xl">
          <h2 className="text-3xl font-bold mb-4">Result</h2>
          <video src={videoUrl} controls className="w-full rounded-md" />
        </div>
      )}

      {code && (
        <div className="mt-8 w-full max-w-2xl">
          <h3 className="text-2xl font-bold mb-2">Generated Code</h3>
          <pre className="bg-gray-800 p-4 rounded-md text-sm whitespace-pre-wrap">
            <code>{code}</code>
          </pre>
        </div>
      )}
    </main>
  );
}