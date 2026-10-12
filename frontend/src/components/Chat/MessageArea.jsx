import { useEffect, useRef } from "react";
import "./MessageArea.css";

function MessageArea({ messages }) {
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
            block: "end",
        });
    }, [messages]);

    return (
        <section
            className="message-area"
            role="log"
            aria-label="Conversation messages"
            aria-live="polite"
        >
            {messages.length === 0 ? (
                <div className="empty-chat">
                    <div className="welcome-icon" aria-hidden="true">
                        ✈
                    </div>
                    <h2>Where would you like to go?</h2>
                    <p>
                        Tell me your destination, travel dates, and
                        preferences.
                    </p>
                </div>
            ) : (
                <div className="message-list">
                    {messages.map((message) => (
                        <article
                            key={message.id}
                            className={`message-row ${message.role}`}
                        >
                            <div className="message-content">
                                <span className="message-author">
                                    {message.role === "human"
                                        ? "You"
                                        : "TripMate AI"}
                                </span>

                                <div className="message-bubble">
                                    {message.content}
                                </div>
                            </div>
                        </article>
                    ))}

                    <div ref={bottomRef} />
                </div>
            )}
        </section>
    );
}

export default MessageArea;