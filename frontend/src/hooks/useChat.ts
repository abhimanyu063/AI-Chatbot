
import { useState, useCallback, useRef, useEffect } from "react";
import type { Message } from "../components/ChatMessage";
import { sendChatMessage } from "../services/api";

// Initial welcome message
const INITIAL_MESSAGE: Message = {
  id: 1,
  role: "assistant",
  content:
    "Hello! I'm your Retail AI Assistant. " +
    "Ask me about sales, profit, competitor performance, " +
    "or product insights.",
};

export function useChat() {
  // Store conversation messages
  const [messages, setMessages] = useState<Message[]>([
    INITIAL_MESSAGE,
  ]);

  // Loading and error states
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Unique IDs for messages
  const nextIdRef = useRef(2);

  // Prevent duplicate requests
  const isRequestActiveRef = useRef(false);

  // Track the active API request
  const abortControllerRef = useRef<AbortController | null>(
    null
  );

  // Unique session for this chat instance
  const sessionIdRef = useRef<string>(
    crypto.randomUUID()
  );

  // Cancel requests when component unmounts
  useEffect(() => {
    return () => {
      abortControllerRef.current?.abort();
    };
  }, []);

  // Send message to Mock API or FastAPI
  const sendMessage = useCallback(async (question: string) => {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || isRequestActiveRef.current) {
      return;
    }

    isRequestActiveRef.current = true;
    setIsLoading(true);
    setError(null);

    // Add user message immediately
    const userMessage: Message = {
      id: nextIdRef.current++,
      role: "user",
      content: trimmedQuestion,
    };

    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);

    // Create a controller for request cancellation
    const controller = new AbortController();
    abortControllerRef.current = controller;

    try {
      // Call services/api.ts
      const response = await sendChatMessage(
        {
          session_id: sessionIdRef.current,
          message: trimmedQuestion,
        },
        controller.signal
      );

      // Ignore a response from a cancelled request
      if (controller.signal.aborted) {
        return;
      }

      // Add AI response to conversation
      const assistantMessage: Message = {
        id: nextIdRef.current++,
        role: "assistant",
        content: response.answer,
      };

      setMessages((previous) => [
        ...previous,
        assistantMessage,
      ]);

    } catch (err) {
      if (!controller.signal.aborted) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to get a response. Please try again."
        );
      }

    } finally {
      // Only reset state for the active request
      if (abortControllerRef.current === controller) {
        abortControllerRef.current = null;
        isRequestActiveRef.current = false;
        setIsLoading(false);
      }
    }
  }, []);

  // Clear conversation and start a fresh session
  const clearChat = useCallback(() => {
    // Cancel any ongoing request
    abortControllerRef.current?.abort();
    abortControllerRef.current = null;
    isRequestActiveRef.current = false;

    // Reset conversation
    setMessages([INITIAL_MESSAGE]);
    setError(null);
    setIsLoading(false);

    // Start a new backend session
    sessionIdRef.current = crypto.randomUUID();
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearChat,
  };
}
