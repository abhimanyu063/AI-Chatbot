
import ChatWidget from "./src/components/ChatWidget";

export default function App() {
  const embedded =
    new URLSearchParams(window.location.search).get("embedded") ===
    "true";

  // When embedded, display only the chatbot
  if (embedded) {
    return <ChatWidget />;
  }

  // Standalone React development page
  return (
    <div className="demo-app">
      <h1>Retail Competitive Intelligence Platform</h1>

      <p>
        Category Manager Dashboard — AI Assistant Development
      </p>

      <ChatWidget />
    </div>
  );
}
