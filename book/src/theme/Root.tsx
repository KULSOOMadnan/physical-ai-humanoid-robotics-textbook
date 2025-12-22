import React from 'react';
import FloatingChatbot from '../components/FloatingChatbot';

// Root wrapper component to add floating chatbot to all pages
export default function Root({ children }) {
  return (
    <>
      {children}
      <FloatingChatbot />
    </>
  );
}