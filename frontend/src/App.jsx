import { useEffect, useState } from "react";
import Sidebar from "./components/Sidebar/Sidebar";
import MessageArea from "./components/Chat/MessageArea";
import MessageBox from "./components/Chat/MessageBox";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function createChat() {
  return {
    id: crypto.randomUUID(),
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
    let cancelled = false;

    async function loadChats() {
      try {
        const response = await fetch(`${API_URL}/chat-histroy`);

        if (!response.ok) {
          throw new Error("Could not load saved chats.");
        }

        const data = await response.json();

        const savedChats = Object.entries(data).map(
          ([threadId, state]) => ({
            id: threadId,
            title: (state.user_query || "Saved chat").slice(0, 50),
            messages: [
              {
                id: crypto.randomUUID(),
                role: "user",
                content: state.user_query || "",
              },
              {
                id: crypto.randomUUID(),
                role: "assistant",
                content: state.itinerary_result || "",
              },
            ].filter((message) => message.content.trim() !== ""),
          })
        );

        if (!cancelled) {
          setChats([initialChat, ...savedChats]);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message);
        }
      } finally {
        if (!cancelled) {
          setHistoryLoading(false);
        }
      }
    }

    loadChats();

    return () => {
      cancelled = true;
    };
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
      id: crypto.randomUUID(),
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
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_query: user_query,
          thread_id: activeChatId,
        }),
      });

      if (!response.ok) {
        throw new Error("Could not generate your itinerary.");
      }

      const data = await response.json();

      const aiMessage = {
        id: activeChatId,
        role: "assistant",
        content: data.itinerary_result
      }

      if (typeof data.itinerary_result !== "string" || !data.itinerary_result.trim()) {
        throw new Error("The backend returned an empty itinerary.");
      }

      setChats((previous) => previous.map((chat) => {
        if (chat.id !== activeChatId) return chat;
        return {
          ...chat,
          title: chat.messages.length === 0 ? user_query.slice(0, 50) : chat.title,
          messages: [...chat.messages, aiMessage]
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