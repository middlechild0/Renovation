"use client";

import DemoSearch from "@/components/DemoSearch";
import Header from "@/components/Header";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <Header />
      <div className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Find Your Perfect Demo
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Search through our production-ready demos and unlock access to see
            how your business can shine online
          </p>
        </div>
        <DemoSearch />
      </div>
    </main>
  );
}
