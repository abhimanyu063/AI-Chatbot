
import { useState } from "react";
import { MessageCircle, X } from "lucide-react";
import ChatWindow from "./ChatWindow";

export default function ChatWidget() {
  // Check whether React is embedded inside Streamlit
  const embedded =
    new URLSearchParams(window.location.search).get("embedded") ===
    "true";

  // Open automatically in embedded mode
  const [isOpen, setIsOpen] = useState(embedded);

  const toggleChat = () => {
    setIsOpen((previous) => !previous);
  };

  return (
    <div
      className={`chat-widget ${embedded ? "embedded" : ""}`}
    >
      {/* Chat window */}
      {isOpen && (
        <div className="chat-window-container">
          <ChatWindow />
        </div>
      )}

      {/* Show launcher only in standalone React mode */}
      {!embedded && (
  <button
    type="button"
    className="chat-toggle-button"
    onClick={toggleChat}
  >
    {isOpen ? <X size={24} /> : <MessageCircle size={24} />}
    <span>{isOpen ? "Close" : "Ask AI"}</span>
  </button>
)}
    </div>
  );
}
