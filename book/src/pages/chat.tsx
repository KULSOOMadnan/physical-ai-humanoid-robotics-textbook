import React from 'react';
import Layout from '@theme/Layout';

// Simple chat page that redirects to floating chatbot
export default function ChatPage() {
  return (
    <Layout
      title={`AI Assistant - Physical AI & Humanoid Robotics Textbook`}
      description="Interactive AI assistant for the Physical AI & Humanoid Robotics Textbook">
      <div className="py-12">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <div className="bg-white rounded-xl shadow-lg p-8 border border-gray-200">
            <div className="text-6xl mb-6">🤖</div>
            <h1 className="text-3xl font-bold text-gray-800 mb-4">AI Assistant</h1>
            <p className="text-lg text-gray-600 mb-6">
              The AI assistant is connected to the RAG system and available as a floating chat widget on every page of the textbook.
            </p>
            <div className="bg-blue-50 rounded-lg p-4 mb-6">
              <p className="text-blue-800">
                <strong>Tip:</strong> Look for the chatbot icon in the bottom right corner of any page.
              </p>
            </div>
            <p className="text-gray-600">
              Click the chat icon to ask questions about the Physical AI & Humanoid Robotics Textbook content.
              The AI assistant can help explain concepts, provide examples, and answer questions based on the textbook material.
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}