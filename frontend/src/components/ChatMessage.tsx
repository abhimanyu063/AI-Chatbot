
import { Bot, User } from "lucide-react";

// Define the message structure
export interface Message {
  id: number;
  role: "user" | "assistant";
  content: string;
}

// Define the props received from ChatWindow
interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({
  message,
}: ChatMessageProps) {
  const isAssistant = message.role === "assistant";

  return (
    <div
      className={`assistant-message ${
        isAssistant ? "assistant" : "user"
      }`}
    >
      {/* Avatar */}
      <div className="message-avatar">
        {isAssistant ? (
          <Bot size={18} />
        ) : (
          <User size={18} />
        )}
      </div>

      {/* Message content */}
      <div className="message-content">
        {message.content}
      </div>
    </div>
  );
}
