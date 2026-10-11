import { useState } from "react";
import "./MessageBox.css";

function MessageBox({ onSend }) {
    const [text, setText] = useState("");

    function handleSubmit(event) {
        event.preventDefault();

        const trimmedText = text.trim();

        if (!trimmedText) return;

        onSend(trimmedText);
        setText("");
    }

    function handleKeyDown(event) {
        if (
            event.key === "Enter" &&
            !event.shiftKey &&
            !event.nativeEvent.isComposing
        ) {
            event.preventDefault();
            event.currentTarget.form.requestSubmit();
        }
    }

    return (
        <div className="message-box-container">
            <form
                className="message-box"
                onSubmit={handleSubmit}
            >
                <textarea
                    value={text}
                    onChange={(event) => setText(event.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask TripMate to plan a trip..."
                    aria-label="Your message"
                    rows={2}
                />

                <button
                    type="submit"
                    disabled={!text.trim()}
                    aria-label="Send message"
                >
                    ↑
                </button>
            </form>

            <p className="input-hint">
                Enter to send · Shift + Enter for a new line
            </p>
        </div>
    );
}

export default MessageBox;