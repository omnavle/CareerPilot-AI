import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const AGENT_LABELS = {
  resume: "Resume Agent",
  career: "Career Agent",
  interview: "Interview Agent",
};

function ChatBubble({ role, text, agent }) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-3`}>
      <div
        className={`max-w-[75%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-indigo-600 text-white rounded-br-sm"
            : "bg-gray-100 text-gray-800 rounded-bl-sm"
        }`}
      >
        {!isUser && agent && (
          <span className="block text-xs font-semibold text-indigo-500 mb-1">
            {AGENT_LABELS[agent] || agent}
          </span>
        )}

        {isUser ? (
          <p className="whitespace-pre-wrap text-sm leading-relaxed">{text}</p>
        ) : (
          <div className="text-sm leading-relaxed markdown-content">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{text}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatBubble;