import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { uploadResume } from "../api/client";

// Job of this file: the Upload page. Lets the user pick a PDF, sends it
// to the backend via uploadResume(), and shows success/error feedback.
// On success, redirects to the Chat page automatically.

function Upload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  function handleFileChange(event) {
    const file = event.target.files[0];
    setSelectedFile(file || null);
    setErrorMessage("");
  }

  async function handleUpload() {
    if (!selectedFile) {
      setErrorMessage("Please choose a PDF file first.");
      return;
    }

    setIsUploading(true);
    setErrorMessage("");

    try {
      await uploadResume(selectedFile);
      // Resume is now parsed and stored - take the user straight to chat
      navigate("/chat");
    } catch (error) {
      // error.response.data.detail comes from our FastAPI HTTPException
      const backendMessage = error.response?.data?.detail;
      setErrorMessage(backendMessage || "Upload failed. Please try again.");
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <div className="max-w-xl mx-auto py-16 px-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-2">Upload Your Resume</h2>
      <p className="text-gray-500 mb-6">We only accept PDF files.</p>

      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center bg-white">
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-indigo-50 file:text-indigo-600 file:font-medium hover:file:bg-indigo-100"
        />

        {selectedFile && (
          <p className="text-sm text-gray-500 mt-3">Selected: {selectedFile.name}</p>
        )}
      </div>

      {errorMessage && (
        <p className="text-red-600 text-sm mt-4">{errorMessage}</p>
      )}

      <button
        onClick={handleUpload}
        disabled={isUploading}
        className="mt-6 w-full bg-indigo-600 text-white py-3 rounded-lg font-medium hover:bg-indigo-700 disabled:bg-gray-300 transition-colors"
      >
        {isUploading ? "Uploading & indexing..." : "Upload Resume"}
      </button>
    </div>
  );
}

export default Upload;
