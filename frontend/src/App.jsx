import { useEffect, useState } from "react";
import Sidebar from "./components/Sidebar/Sidebar";
import MessageArea from "./components/Chat/MessageArea";
import MessageBox from "./components/Chat/MessageBox";
import "./App.css";

//const API_URL = "http://127.0.0.1:8000";
const API_URL = "/api";

function createId() {
  if (typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }

  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function createChat() {
  return {
    id: createId(),
    title: "New chat",
    messages: [],
  };
}

function App() {
  const [initialChat] = useState(createChat);

  const [chats, setChats] = useState([initialChat]);
  const [activeChatId, setActiveChatId] = useState(initialChat.id);

  const [historyLoading, setHistoryLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {

    async function loadChats() {
      try {
        const response = await fetch(`${API_URL}/all-chat-history`);
        if (!response.ok) throw new Error("Could not load saved chats");
        const data = await response.json();

        const savedChats = Object.entries(data).map(([threadId, values]) => {

          const allMessages = values.messages || []

          const filteredMessages = allMessages.filter((message) => {
            if (message.type === "human") return true;

            if (message.type === "ai" && (message.name === "itinerary_node" || message.name === "guardrail_node" || message.name === "supervisor_node")) return true;

            return false;
          })

          const messages = filteredMessages.map((message) => {
            return {
              id: message.id,
              role: message.type,
              content: message.content
            }
          })

          return {
            id: threadId,
            title: messages[0]?.content.slice(0, 50) || "New Chat",
            messages
          }
        })

        setChats([initialChat, ...savedChats]);

      } catch (err) {
        console.error("Error loading chats:", err);
        setError("Failed to load chats. Please try again later.");
      } finally {
        setHistoryLoading(false);
      }
    }

    loadChats()
  }, [initialChat]);

  function handleNewChat() {
    const emptyChat = chats.find((chat) => chat.messages.length === 0);
    if (emptyChat) {
      setActiveChatId(emptyChat.id);
      return;
    }
    const newChat = createChat();

    setChats((previous) => [newChat, ...previous]);
    setActiveChatId(newChat.id);
    setError("");
  }

  async function handleSend(text) {

    const user_query = text.trim();
    if (!user_query) return;

    const userMessage = {
      id: createId(),
      role: "user",
      content: user_query,
    }

    setChats((previous) => previous.map((chat) => {
      if (chat.id !== activeChatId) return chat;
      return {
        ...chat,
        title: chat.messages.length === 0 ? user_query.slice(0, 50) : chat.title,
        messages: [...chat.messages, userMessage]
      }
    }))

    setError("");

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_query: user_query,
          thread_id: activeChatId,
        }),
      });

      if (!response.ok) {
        throw new Error("Could not generate your itinerary.");
      }

      const data = await response.json();

      if (!Array.isArray(data.messages)) {
        throw new Error("The backend returned invalid messages.");
      }

      const filteredMessages = data.messages.filter((message) => {
        if (message.type === "human") return true;

        if (message.type === "ai" && (message.name === "itinerary_node" || message.name === "guardrail_node" || message.name === "supervisor_node")) return true;

        return false;
      })

      const messages = filteredMessages.map((message) => {
        return {
          id: message.id,
          role: message.type,
          content: message.content
        }
      })

      setChats((previous) => previous.map((chat) => {
        if (chat.id !== activeChatId) return chat;
        return {
          ...chat,
          messages: [...messages]
        }
      }))
    } catch (err) {
      setError(err.message);
    }
  }

  const activeChat = chats.find((chat) => chat.id === activeChatId);

  if (historyLoading) {
    return <p role="status">Loading your conversations…</p>;
  }

  return (
    <div className="app">
      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        onSelectChat={setActiveChatId}
        onNewChat={handleNewChat}
      />

      <main className="chat-panel">
        <header className="chat-header">
          <h1>TripMate AI</h1>
          <span>Your travel planning assistant</span>
        </header>

        {error && (
          <p
            role="alert"
            style={{ padding: "0 28px", color: "#b91c1c" }}
          >
            {error}
          </p>
        )}

        <MessageArea messages={activeChat?.messages || []} />

        <MessageBox
          key={activeChatId}
          onSend={handleSend}
        />

      </main>
    </div>
  );
}

export default App;