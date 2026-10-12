
import { useState, type FormEvent } from "react";
import { Bot, Send, Trash2 } from "lucide-react";

import { useChat } from "../hooks/useChat";
import ChatMessage from "./ChatMessage";

// Suggested questions for Category Managers
const suggestedQuestions = [
  "Why are Target sales declining?",
  "Compare Target vs Amazon pricing",
  "What factors affect product profitability?",
];

export default function ChatWindow() {
  // Chat business logic comes from our custom hook
  const {
    messages,
    isLoading,
    error,
    sendMessage,
    clearChat,
  } = useChat();

  // Only UI input state is managed here
  const [input, setInput] = useState("");

  // Handle user sending a message
  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const question = input.trim();

    if (!question || isLoading) {
      return;
    }

    setInput("");
    void sendMessage(question);
  };

  // Handle suggested question click
  const handleSuggestedQuestion = (question: string) => {
    if (isLoading) {
      return;
    }

    void sendMessage(question);
  };

  // Clear chat history and input
  const handleClearChat = () => {
    clearChat();
    setInput("");
  };

  return (
    <div className="assistant-window">

      {/* ================= HEADER ================= */}
      <div className="assistant-header">
        <div className="assistant-title">
          <Bot size={24} />

          <div>
            <strong>Retail AI Assistant</strong>
            <small>Competitive Intelligence</small>
          </div>
        </div>

        <button
          type="button"
          className="assistant-clear"
          onClick={handleClearChat}
          title="Clear conversation"
          aria-label="Clear conversation"
          disabled={isLoading}
        >
          <Trash2 size={18} />
        </button>
      </div>

      {/* ================= MESSAGES ================= */}
      <div
        className="assistant-messages"
        role="log"
        aria-live="polite"
        aria-label="Chat messages"
      >
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message}
          />
        ))}

        {/* Loading indicator */}
        {isLoading && (
          <div
            className="assistant-loading"
            role="status"
          >
            <Bot size={18} />
            <span>AI Assistant is thinking...</span>
          </div>
        )}

        {/* Error message */}
        {error && (
          <div
            className="assistant-error"
            role="alert"
          >
            {error}
          </div>
        )}
      </div>

      {/* ================= SUGGESTED QUESTIONS ================= */}
      {messages.length === 1 && !isLoading && (
        <div className="assistant-suggestions">
          {suggestedQuestions.map((question) => (
            <button
              key={question}
              type="button"
              onClick={() =>
                handleSuggestedQuestion(question)
              }
            >
              {question}
            </button>
          ))}
        </div>
      )}

      {/* ================= CHAT INPUT ================= */}
      <form
        className="assistant-input-area"
        onSubmit={handleSubmit}
      >
        <input
          type="text"
          value={input}
          onChange={(event) =>
            setInput(event.target.value)
          }
          placeholder="Ask about sales, competitors..."
          aria-label="Your question"
          disabled={isLoading}
        />

        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          aria-label="Send message"
        >
          <Send size={20} />
        </button>
      </form>

      {/* ================= FOOTER ================= */}
      <div className="assistant-footer">
        AI-generated insights should be verified
        against source data.
      </div>

    </div>
  );
}
