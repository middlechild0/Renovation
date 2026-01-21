"use client";

import { useState } from "react";
import PaymentModal from "./PaymentModal";

interface DemoCardProps {
  demo: {
    id: string;
    business_name: string;
    industry: string;
    tier: string;
    demo_url: string;
    status: string;
  };
}

const tierColors = {
  "1": "bg-green-100 text-green-800",
  "2": "bg-blue-100 text-blue-800",
  "3": "bg-purple-100 text-purple-800",
};

const tierNames = {
  "1": "Basic",
  "2": "Professional",
  "3": "Premium",
};

export default function DemoCard({ demo }: DemoCardProps) {
  const [showPayment, setShowPayment] = useState(false);
  const tierColor =
    tierColors[demo.tier as keyof typeof tierColors] ||
    "bg-gray-100 text-gray-800";
  const tierName = tierNames[demo.tier as keyof typeof tierNames] || "Standard";

  return (
    <>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
        {/* Demo Preview Section */}
        <div className="h-48 bg-gradient-to-br from-primary-100 to-primary-200 p-6 flex items-center justify-center">
          <div className="text-center">
            <div className="text-4xl mb-2">🌐</div>
            <p className="text-sm text-primary-800 font-medium">
              Live Demo Available
            </p>
          </div>
        </div>

        {/* Content Section */}
        <div className="p-6">
          <div className="flex items-start justify-between mb-3">
            <h3 className="text-xl font-bold text-gray-900">
              {demo.business_name}
            </h3>
            <span
              className={`px-3 py-1 rounded-full text-xs font-semibold ${tierColor}`}
            >
              Tier {demo.tier}
            </span>
          </div>

          <div className="space-y-2 mb-4">
            <div className="flex items-center gap-2 text-gray-600">
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                />
              </svg>
              <span className="capitalize">{demo.industry}</span>
            </div>

            <div className="flex items-center gap-2 text-gray-600">
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span
                className={
                  demo.status === "success" ? "text-green-600" : "text-gray-600"
                }
              >
                {demo.status === "success" ? "Production Ready" : demo.status}
              </span>
            </div>
          </div>

          {/* Features List */}
          <div className="mb-4 pb-4 border-b border-gray-200">
            <p className="text-sm text-gray-600 mb-2 font-semibold">
              Includes:
            </p>
            <ul className="text-sm text-gray-600 space-y-1">
              <li className="flex items-center gap-2">
                <span className="text-green-500">✓</span> Responsive Design
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500">✓</span> Custom Color Palette
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500">✓</span> Live Deployment
              </li>
            </ul>
          </div>

          {/* Price and CTA */}
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Access Fee</p>
              <p className="text-2xl font-bold text-gray-900">$50</p>
            </div>
            <button
              onClick={() => setShowPayment(true)}
              className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold"
            >
              Get Access
            </button>
          </div>
        </div>
      </div>

      {showPayment && (
        <PaymentModal demo={demo} onClose={() => setShowPayment(false)} />
      )}
    </>
  );
}
