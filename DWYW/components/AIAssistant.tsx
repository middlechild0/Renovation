/**
 * AI Design Assistant Component
 * 
 * Natural language interface for design modifications
 */

'use client';

import { useState, useRef, useEffect } from 'react';
import { useProjectStore } from '@/store/project';
import { AIAnalysisEngine } from '@/lib/ai-assistant';
import { motion, AnimatePresence } from 'framer-motion';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export function AIAssistant() {
  const { design, updateDesign, analysis, runAnalysis, isAnalyzing } = useProjectStore();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: "Hi! I'm your AI design assistant. I can help you customize colors, fonts, spacing, and more. Try saying something like 'Make the primary color blue' or 'Use a modern font'.",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || !design) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsThinking(true);

    try {
      // Parse the natural language request
      const parsedRequest = AIAnalysisEngine.parseDesignRequest(input);
      
      // Apply the changes
      const updates: any = {};
      
      if (parsedRequest.colors) {
        updates.colors = { ...design.colors, ...parsedRequest.colors };
      }
      
      if (parsedRequest.fonts) {
        updates.fonts = { ...design.fonts, ...parsedRequest.fonts };
      }
      
      if (parsedRequest.spacing !== undefined) {
        updates.spacing = parsedRequest.spacing;
      }
      
      if (parsedRequest.borderRadius !== undefined) {
        updates.borderRadius = parsedRequest.borderRadius;
      }
      
      if (parsedRequest.animations) {
        updates.animations = { ...design.animations, ...parsedRequest.animations };
      }

      updateDesign(updates);

      // Generate response
      let response = "I've updated your design! ";
      
      if (parsedRequest.colors) {
        const colorKeys = Object.keys(parsedRequest.colors);
        response += `Changed ${colorKeys.join(', ')} color${colorKeys.length > 1 ? 's' : ''}. `;
      }
      
      if (parsedRequest.fonts) {
        const fontKeys = Object.keys(parsedRequest.fonts);
        response += `Updated ${fontKeys.join(', ')} font${fontKeys.length > 1 ? 's' : ''}. `;
      }
      
      if (parsedRequest.spacing !== undefined) {
        response += `Adjusted spacing to ${parsedRequest.spacing}x. `;
      }
      
      if (parsedRequest.borderRadius !== undefined) {
        response += `Set border radius to ${parsedRequest.borderRadius}px. `;
      }

      response += "How does it look?";

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "I'm sorry, I didn't quite understand that. Could you try rephrasing? For example, try 'Make the background darker' or 'Use a playful font'.",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsThinking(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const suggestedPrompts = [
    'Make the design more modern',
    'Use warmer colors',
    'Increase spacing',
    'Make corners more rounded',
    'Add subtle animations',
  ];

  return (
    <div className="h-full flex flex-col bg-white border-l border-gray-200">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
            <span className="text-white text-xl">✨</span>
          </div>
          <div>
            <h3 className="font-semibold">AI Design Assistant</h3>
            <p className="text-xs text-gray-500">Powered by AI</p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] px-4 py-3 rounded-2xl ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-900'
                }`}
              >
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                <p
                  className={`text-xs mt-1 ${
                    message.role === 'user' ? 'text-blue-200' : 'text-gray-500'
                  }`}
                >
                  {message.timestamp.toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {isThinking && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex justify-start"
          >
            <div className="bg-gray-100 px-4 py-3 rounded-2xl">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
              </div>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Prompts */}
      {messages.length <= 2 && (
        <div className="px-4 pb-2">
          <p className="text-xs text-gray-500 mb-2">Try asking:</p>
          <div className="flex flex-wrap gap-2">
            {suggestedPrompts.map((prompt, index) => (
              <button
                key={index}
                onClick={() => setInput(prompt)}
                className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded-full transition-colors"
              >
                {prompt}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Analysis Button */}
      <div className="px-4 pb-2">
        <button
          onClick={runAnalysis}
          disabled={isAnalyzing}
          className="w-full py-2 bg-purple-600 text-white rounded-lg font-medium hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isAnalyzing ? 'Analyzing...' : '🔍 Run Design Analysis'}
        </button>
        
        {analysis && (
          <div className="mt-3 p-3 bg-gray-50 rounded-lg text-sm space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Usability</span>
              <span className={`font-semibold ${
                analysis.scores.usability >= 80 ? 'text-green-600' : 
                analysis.scores.usability >= 60 ? 'text-yellow-600' : 'text-red-600'
              }`}>
                {analysis.scores.usability}/100
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Accessibility</span>
              <span className={`font-semibold ${
                analysis.scores.accessibility >= 80 ? 'text-green-600' : 
                analysis.scores.accessibility >= 60 ? 'text-yellow-600' : 'text-red-600'
              }`}>
                {analysis.scores.accessibility}/100
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">SEO</span>
              <span className={`font-semibold ${
                analysis.scores.seo >= 80 ? 'text-green-600' : 
                analysis.scores.seo >= 60 ? 'text-yellow-600' : 'text-red-600'
              }`}>
                {analysis.scores.seo}/100
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Performance</span>
              <span className={`font-semibold ${
                analysis.scores.performance >= 80 ? 'text-green-600' : 
                analysis.scores.performance >= 60 ? 'text-yellow-600' : 'text-red-600'
              }`}>
                {analysis.scores.performance}/100
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-200">
        <div className="flex space-x-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Describe what you want to change..."
            rows={2}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isThinking}
            className="px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
