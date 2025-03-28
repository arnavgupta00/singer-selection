import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center text-center">
      <h1 className="text-5xl font-bold mb-4">Welcome to the Singing Evaluation System</h1>
      <p className="text-lg mb-6">Capture your singing and get an AI-driven evaluation instantly.</p>
      <Link
        href="/record"
        className="px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-500 transition"
      >
        Go to Recording Page
      </Link>
    </div>
  );
}
