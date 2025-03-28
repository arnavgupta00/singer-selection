"use client";
// pages/record.tsx
import React from 'react'
import AudioRecorder from '@/components/AudioRecorder';

const RecordPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-6">Record Your Singing</h1>
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
        <AudioRecorder />
      </div>
    </div>
  );
};

export default RecordPage;
