import "./Sidebar.css";

function Sidebar({
    chats,
    activeChatId,
    onSelectChat,
    onNewChat,
}) {
    return (
        <aside className="sidebar">
            <div className="sidebar-brand">TripMate ✈</div>

            <button
                type="button"
                className="new-chat-button"
                onClick={onNewChat}
            >
                + New chat
            </button>

            <p className="sidebar-label">Conversations</p>

            <nav className="chat-list" aria-label="Chat history">
                {chats.map((chat) => (
                    <button
                        key={chat.id}
                        type="button"
                        className={`chat-item ${chat.id === activeChatId ? "active" : ""}`}
                        aria-current={chat.id === activeChatId ? "page" : undefined}
                        title={chat.title}
                        onClick={() => onSelectChat(chat.id)}
                    >
                        {`${chat.title}`}
                    </button>
                ))}
            </nav>

            <div className="sidebar-footer">
                Plan your next adventure
            </div>
        </aside>
    );
}

export default Sidebar;