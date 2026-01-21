"use client";

import { useState } from "react";
import DemoCard from "./DemoCard";
import axios from "axios";

interface Demo {
  id: string;
  business_name: string;
  industry: string;
  tier: string;
  demo_url: string;
  status: string;
}

export default function DemoSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Demo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const searchDemos = async () => {
    if (!query.trim()) {
      setError("Please enter a search term");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post("/api/demos/search", { query });
      setResults(response.data);

      if (response.data.length === 0) {
        setError(
          'No demos found. Try searching for "Java House", "Dental", or "Tech"',
        );
      }
    } catch (err) {
      setError("Failed to search demos. Please try again.");
      console.error("Search error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      searchDemos();
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Search Bar */}
      <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
        <div className="flex gap-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Search by business name or industry (e.g., Java House, Dental, Restaurant)..."
            className="flex-1 p-4 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:outline-none text-lg"
          />
          <button
            onClick={searchDemos}
            disabled={loading}
            className="px-8 py-4 bg-primary-600 text-white rounded-xl hover:bg-primary-700 transition-colors font-semibold disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                    fill="none"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                Searching...
              </span>
            ) : (
              "Search"
            )}
          </button>
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded">
            <p className="font-medium">{error}</p>
          </div>
        )}
      </div>

      {/* Results Grid */}
      {results.length > 0 && (
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Found {results.length} {results.length === 1 ? "demo" : "demos"}
          </h2>
        </div>
      )}

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {results.map((demo) => (
          <DemoCard key={demo.id} demo={demo} />
        ))}
      </div>

      {/* Example Searches */}
      {results.length === 0 && !loading && !error && (
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <h3 className="text-xl font-semibold mb-4 text-gray-800">
            Try these example searches:
          </h3>
          <div className="flex flex-wrap gap-3">
            {["Java House", "Dental", "Restaurant", "Tech", "Medical"].map(
              (term) => (
                <button
                  key={term}
                  onClick={() => {
                    setQuery(term);
                    setTimeout(() => searchDemos(), 100);
                  }}
                  className="px-4 py-2 bg-gray-100 hover:bg-primary-100 rounded-lg text-gray-700 hover:text-primary-700 transition-colors"
                >
                  {term}
                </button>
              ),
            )}
          </div>
        </div>
      )}
    </div>
  );
}
