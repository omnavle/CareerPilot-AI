import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="max-w-2xl mx-auto text-center py-20 px-6">
      <h1 className="text-4xl font-bold text-gray-800 mb-4">
        Welcome to <span className="text-indigo-600">CareerPilot AI</span>
      </h1>
      <p className="text-gray-600 text-lg mb-8">
        Upload your resume and chat with an AI career coach that gives you
        resume feedback, career advice, and interview questions - all based
        on your actual resume.
      </p>
      <Link
        to="/upload"
        className="inline-block bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700 transition-colors"
      >
        Get Started - Upload Resume
      </Link>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-14 text-left">
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h3 className="font-semibold text-gray-800 mb-1">📄 Resume Review</h3>
          <p className="text-sm text-gray-500">Get feedback and improvement suggestions.</p>
        </div>
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h3 className="font-semibold text-gray-800 mb-1">🎯 Career Advice</h3>
          <p className="text-sm text-gray-500">Skill gaps, roadmaps, and project ideas.</p>
        </div>
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h3 className="font-semibold text-gray-800 mb-1">🎤 Interview Prep</h3>
          <p className="text-sm text-gray-500">Practice with questions based on your resume.</p>
        </div>
      </div>
    </div>
  );
}

export default Home;
