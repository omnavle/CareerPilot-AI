import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:8000",
});

/**
 * Uploads a resume PDF to the backend.
 * @param {File} file - the PDF file selected by the user
 * @returns {Promise} resolves to { message, filename, chunks_stored }
 */
export async function uploadResume(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await apiClient.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
}

/**
 * Sends a chat question to the backend's LangGraph workflow.
 * @param {string} question - the user's typed question
 * @returns {Promise} resolves to { agent, answer, sources }
 */
export async function sendChatMessage(question) {
  const response = await apiClient.post("/chat", { question });
  return response.data;
}
export async function streamChatMessage(question, { onAgent, onChunk, onDone, onError }) {
  try {
    const response = await fetch("http://localhost:8000/chat/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => null);
      onError?.(errorBody?.detail || "Something went wrong. Please try again.");
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      const lines = buffer.split("\n");
      buffer = lines.pop();

      for (const line of lines) {
        if (!line.trim()) continue;
        const event = JSON.parse(line);

        if (event.type === "agent") {
          onAgent?.(event.agent);
        } else if (event.type === "chunk") {
          onChunk?.(event.text);
        } else if (event.type === "sources") {
          onDone?.(event.sources);
        }
      }
    }
  } catch (error) {
    onError?.("Connection error. Please check the backend is running.");
  }
}

/**
 * Checks whether a resume has already been uploaded.
 * @returns {Promise} resolves to { resume_uploaded, filename }
 */
export async function getResumeStatus() {
  const response = await apiClient.get("/resume");
  return response.data;
}

export default apiClient;
