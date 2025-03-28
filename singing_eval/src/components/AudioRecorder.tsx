// components/AudioRecorder.tsx
import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';

const AudioRecorder: React.FC = () => {
  const [recording, setRecording] = useState(false);
  const [audioChunks, setAudioChunks] = useState<Blob[]>([]);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);

  useEffect(() => {
    let stream: MediaStream;
    const startRecording = async () => {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          setAudioChunks((prev) => [...prev, event.data]);
        }
      };

      mediaRecorderRef.current.start();
    };

    if (recording) {
      startRecording();
    }

    return () => {
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stop();
      }
      if (stream) {
        stream.getAudioTracks().forEach((track) => track.stop());
      }
    };
  }, [recording]);

  const handleStart = () => {
    setAudioChunks([]);
    setRecording(true);
  };

  const handleStop = async () => {
    setRecording(false);
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
  };

  const handleSend = async () => {
    if (audioChunks.length === 0) return;
    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
    
    // Convert to a form data for sending to the backend
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.webm');

    try {
      const response = await axios.post('http://localhost:8000/evaluate', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      console.log('Evaluation result:', response.data);
      alert('Score: ' + response.data.score + '\nRanking: ' + response.data.rank);
    } catch (err) {
      console.error('Error uploading file:', err);
    }
  };

  return (
    <div className="text-center">
      <h2 className="text-2xl font-semibold mb-4">Singing Evaluation Recorder</h2>
      <div className="space-x-4">
        {!recording && (
          <button
            onClick={handleStart}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-500 transition"
          >
            Start Recording
          </button>
        )}
        {recording && (
          <button
            onClick={handleStop}
            className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-500 transition"
          >
            Stop Recording
          </button>
        )}
        <button
          onClick={handleSend}
          disabled={recording || audioChunks.length === 0}
          className={`px-4 py-2 rounded transition ${
            recording || audioChunks.length === 0
              ? "bg-gray-600 text-gray-400 cursor-not-allowed"
              : "bg-blue-600 text-white hover:bg-blue-500"
          }`}
        >
          Send for Evaluation
        </button>
      </div>
    </div>
  );
};

export default AudioRecorder;
