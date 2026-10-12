
/**
 * Retail Competitive Intelligence - Chat API
 *
 * Supports:
 * 1. Mock responses for frontend development
 * 2. Real FastAPI backend integration
 */

export interface DashboardContext {
  productId?: string;
  productName?: string;
  category?: string;
  dateRange?: string;
}

export interface ChatRequest {
  session_id: string;
  message: string;
  dashboard_context?: DashboardContext;
}

export interface Citation {
  title: string;
  url: string;
  source?: string;
}

export interface ChatResponse {
  answer: string;
  citations: Citation[];
}

// Vite environment variables
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://localhost:8000";

const USE_MOCK_API =
  import.meta.env.VITE_USE_MOCK_API !== "false";

// Mock response generator
function getMockResponse(question: string): ChatResponse {
  const query = question.toLowerCase();

  if (
    query.includes("amazon") ||
    query.includes("walmart") ||
    query.includes("competitor")
  ) {
    return {
      answer:
        "[MOCK RESPONSE]\n\n" +
        "The AI Assistant will compare Target products " +
        "against competitors using pricing, promotions, " +
        "availability, and other external signals.\n\n" +
        "The Research Agent will collect supporting evidence " +
        "and citations before generating recommendations.",
      citations: [],
    };
  }

  if (
    query.includes("sales") ||
    query.includes("declining")
  ) {
    return {
      answer:
        "[MOCK RESPONSE]\n\n" +
        "Step 1: Retrieve Target sales data through " +
        "the existing SQL Planner API.\n\n" +
        "Step 2: Check data completeness using the Coverage Gate.\n\n" +
        "Step 3: Trigger competitor research only when " +
        "required signals are missing.\n\n" +
        "Step 4: Generate comparative analysis and RCA.",
      citations: [],
    };
  }

  if (
    query.includes("profit") ||
    query.includes("margin")
  ) {
    return {
      answer:
        "[MOCK RESPONSE]\n\n" +
        "I can analyze internal profit, margin, " +
        "and sales trends and combine them with " +
        "available competitor evidence.",
      citations: [],
    };
  }

  return {
    answer:
      "[MOCK RESPONSE]\n\n" +
      "Your question has been received. " +
      "The AI Intelligence Engine will interpret the query, " +
      "retrieve relevant data, and generate evidence-backed insights.",
    citations: [],
  };
}

// Simulate network latency
function delay(milliseconds: number): Promise<void> {
  return new Promise((resolve) =>
    setTimeout(resolve, milliseconds)
  );
}

/**
 * Send user message to AI Assistant
 */
export async function sendChatMessage(
  request: ChatRequest,
  signal?: AbortSignal
): Promise<ChatResponse> {
  if (!request.message.trim()) {
    throw new Error("Message cannot be empty.");
  }

  // Mock mode
  if (USE_MOCK_API) {
    await delay(500);

    if (signal?.aborted) {
      throw new DOMException("Request cancelled", "AbortError");
    }

    return getMockResponse(request.message);
  }

  // Real FastAPI mode
  const response = await fetch(
    `${API_BASE_URL}/api/v1/assistant/chat`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
      signal,
    }
  );

  if (!response.ok) {
    throw new Error(
      `Chat API failed with status ${response.status}`
    );
  }

  const data: unknown = await response.json();

  // Basic response validation
  if (
    typeof data !== "object" ||
    data === null ||
    !("answer" in data) ||
    typeof data.answer !== "string" ||
    !("citations" in data) ||
    !Array.isArray(data.citations)
  ) {
    throw new Error("Invalid response from AI backend.");
  }

  return data as ChatResponse;
}
