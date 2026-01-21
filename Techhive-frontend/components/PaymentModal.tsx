"use client";

import { useState } from "react";
import { loadStripe } from "@stripe/stripe-js";
import {
  Elements,
  PaymentElement,
  useStripe,
  useElements,
} from "@stripe/react-stripe-js";
import axios from "axios";

const stripePromise = loadStripe(
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!,
);

interface PaymentModalProps {
  demo: {
    id: string;
    business_name: string;
    demo_url: string;
  };
  onClose: () => void;
}

function CheckoutForm({ demo, onClose }: PaymentModalProps) {
  const stripe = useStripe();
  const elements = useElements();
  const [email, setEmail] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [processing, setProcessing] = useState(false);
  const [succeeded, setSucceeded] = useState(false);
  const [accessUrl, setAccessUrl] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!stripe || !elements || !email) {
      return;
    }

    setProcessing(true);
    setError(null);

    try {
      // Create payment intent
      const { data } = await axios.post("/api/payments/create", {
        demo_id: demo.id,
        client_email: email,
      });

      // Confirm payment
      const { error: stripeError } = await stripe.confirmPayment({
        elements,
        confirmParams: {
          return_url: window.location.origin + "/payment-success",
        },
        redirect: "if_required",
      });

      if (stripeError) {
        setError(stripeError.message || "Payment failed");
        setProcessing(false);
        return;
      }

      // Payment succeeded
      setSucceeded(true);
      setAccessUrl(demo.demo_url);

      // Send confirmation email (handled by backend)
      await axios.post("/api/payments/confirm", {
        demo_id: demo.id,
        client_email: email,
      });
    } catch (err: any) {
      setError(err.response?.data?.error || "Payment processing failed");
      setProcessing(false);
    }
  };

  if (succeeded) {
    return (
      <div className="text-center py-8">
        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg
            className="w-8 h-8 text-green-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          Payment Successful!
        </h3>
        <p className="text-gray-600 mb-6">
          You now have access to {demo.business_name}
        </p>

        <div className="bg-primary-50 border border-primary-200 rounded-lg p-4 mb-6">
          <p className="text-sm text-gray-600 mb-2">Your Demo URL:</p>
          <a
            href={accessUrl || "#"}
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary-600 hover:text-primary-700 font-medium break-all"
          >
            {accessUrl}
          </a>
        </div>

        <button
          onClick={onClose}
          className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold"
        >
          Close
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label
          htmlFor="email"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Email Address
        </label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          placeholder="your@email.com"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Payment Details
        </label>
        <PaymentElement />
      </div>

      {error && (
        <div className="p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded">
          <p className="font-medium">{error}</p>
        </div>
      )}

      <div className="flex gap-4">
        <button
          type="button"
          onClick={onClose}
          className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-semibold"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={!stripe || processing}
          className="flex-1 px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {processing ? "Processing..." : "Pay $50"}
        </button>
      </div>
    </form>
  );
}

export default function PaymentModal({ demo, onClose }: PaymentModalProps) {
  const [clientSecret, setClientSecret] = useState<string | null>(null);

  // Fetch client secret when modal opens
  useState(() => {
    axios
      .post("/api/payments/create", {
        demo_id: demo.id,
        client_email: "placeholder@example.com",
      })
      .then(({ data }) => {
        setClientSecret(data.client_secret);
      })
      .catch((err) => {
        console.error("Failed to create payment intent:", err);
      });
  });

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">
            Complete Purchase
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        <div className="mb-6 pb-6 border-b border-gray-200">
          <p className="text-gray-600 mb-2">Demo</p>
          <p className="text-lg font-semibold text-gray-900">
            {demo.business_name}
          </p>
        </div>

        {clientSecret && (
          <Elements stripe={stripePromise} options={{ clientSecret }}>
            <CheckoutForm demo={demo} onClose={onClose} />
          </Elements>
        )}

        {!clientSecret && (
          <div className="flex justify-center py-8">
            <svg
              className="animate-spin h-8 w-8 text-primary-600"
              viewBox="0 0 24 24"
            >
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
          </div>
        )}
      </div>
    </div>
  );
}
