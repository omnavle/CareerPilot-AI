import { useEffect, useState } from "react";
import ChatBubble from "../components/ChatBubble";

// Job of this file: an OPTIONAL, simple History page.
// Instead of adding a database table just to store chat history
// (overkill for a fresher project), we just read the last saved
// conversation from the browser's localStorage, which Chat.jsx writes to.

function History() {
  const [historyEntry, setHistoryEntry] = useState(null);

  useEffect(() => {
    const saved = localStorage.getItem("careerpilot_history");
    if (saved) {
      setHistoryEntry(JSON.parse(saved));
    }
  }, []);

  if (!historyEntry) {
    return (
      <div className="max-w-xl mx-auto py-20 text-center text-gray-500">
        No chat history yet. Start a conversation on the Chat page.
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto py-8 px-6">
      <h2 className="text-xl font-bold text-gray-800 mb-1">Last Conversation</h2>
      <p className="text-sm text-gray-400 mb-4">
        {new Date(historyEntry.timestamp).toLocaleString()}
      </p>
      <div className="bg-gray-50 rounded-lg p-4">
        {historyEntry.messages.map((message, index) => (
          <ChatBubble
            key={index}
            role={message.role}
            text={message.text}
            agent={message.agent}
          />
        ))}
      </div>
    </div>
  );
}

export default History;
