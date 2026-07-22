import { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import { streamChatMessage, getResumeStatus } from "../api/client";
import ChatBubble from "../components/ChatBubble";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [resumeUploaded, setResumeUploaded] = useState(true);
  
  const messagesContainerRef = useRef(null);

useEffect(() => {
  getResumeStatus().then((status) => {
    setResumeUploaded(status.resume_uploaded);
  });
}, []);


useEffect(() => {
  const container = messagesContainerRef.current;
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
}, [messages]);

  async function handleSend() {
    const question = inputText.trim();
    if (!question || isSending) return;

    const userMessage = { role: "user", text: question };
    const aiMessage = { role: "ai", text: "", agent: null };

    setMessages((prev) => [...prev, userMessage, aiMessage]);
    setInputText("");
    setIsSending(true);

    const aiMessageIndex = messages.length + 1;

    streamChatMessage(question, {
      onAgent: (agentName) => {
        setMessages((prev) => {
          const updated = [...prev];
          updated[aiMessageIndex] = { ...updated[aiMessageIndex], agent: agentName };
          return updated;
        });
      },
      onChunk: (textPiece) => {
        setMessages((prev) => {
          const updated = [...prev];
          updated[aiMessageIndex] = {
            ...updated[aiMessageIndex],
            text: updated[aiMessageIndex].text + textPiece,
          };
          return updated;
        });
      },
      onDone: (sources) => {
        setIsSending(false);
        setMessages((prev) => {
          saveToHistory(prev);
          return prev;
        });
      },
      onError: (errorMessage) => {
        setIsSending(false);
        setMessages((prev) => {
          const updated = [...prev];
          updated[aiMessageIndex] = { role: "ai", text: errorMessage };
          return updated;
        });
      },
    });
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  }

  function saveToHistory(allMessages) {
    const historyEntry = {
      timestamp: new Date().toISOString(),
      messages: allMessages,
    };
    localStorage.setItem("careerpilot_history", JSON.stringify(historyEntry));
  }

  if (!resumeUploaded) {
    return (
      <div className="max-w-xl mx-auto py-20 text-center">
        <p className="text-gray-600 mb-4">
          You haven't uploaded a resume yet. Please upload one to start chatting.
        </p>
        <Link
          to="/upload"
          className="inline-block bg-indigo-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-indigo-700"
        >
          Go to Upload
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto py-8 px-6 flex flex-col h-[calc(100vh-64px)]">
      <h2 className="text-xl font-bold text-gray-800 mb-4">Chat with your Career Coach</h2>

      <div
  ref={messagesContainerRef}
  className="flex-1 overflow-y-auto bg-gray-50 rounded-lg p-4 mb-4"
>
  {messages.length === 0 && (
    <p className="text-gray-400 text-sm text-center mt-10">
      Try asking: "Improve my resume", "What skills should I learn?",
      or "Generate interview questions"
    </p>
  )}
  {messages.map((message, index) => (
    <ChatBubble
      key={index}
      role={message.role}
      text={message.text}
      agent={message.agent}
    />
  ))}
</div>

      <div className="flex gap-2">
        <textarea
          value={inputText}
          onChange={(event) => setInputText(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about your resume, career, or interview prep..."
          rows={2}
          className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <button
          onClick={handleSend}
          disabled={isSending}
          className="bg-indigo-600 text-white px-5 rounded-lg font-medium hover:bg-indigo-700 disabled:bg-gray-300"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default Chat;