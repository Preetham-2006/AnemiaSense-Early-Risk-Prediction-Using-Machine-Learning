import { useState } from "react";
import { MessageCircle, X, Send } from "lucide-react";

import API from "../api";

export default function Chatbot() {

  const [open, setOpen] = useState(false);

  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text:
        "Hi! I'm your AnemiaSense health assistant. Ask me about CBC parameters, your report, or blood health."
    }
  ]);

  const sendMessage = async () => {

    if (!message.trim()) return;

    const userMessage = message;

    setMessages((old) => [
      ...old,
      {
        role: "user",
        text: userMessage
      }
    ]);

    setMessage("");

    try {

      const response = await API.post(
        "/chat",
        {
          message: userMessage
        }
      );

      setMessages((old) => [
        ...old,
        {
          role: "assistant",
          text: response.data.response
        }
      ]);

    } catch {

      setMessages((old) => [
        ...old,
        {
          role: "assistant",
          text:
            "Sorry, I could not process that question right now."
        }
      ]);

    }
  };

  if (!open) {

    return (
      <button
        className="chat-launcher"
        onClick={() => setOpen(true)}
      >
        <MessageCircle size={24} />
      </button>
    );

  }

  return (
    <div className="chat-window">

      <div className="chat-header">

        <div>
          <strong>AI Health Assistant</strong>
          <small>General CBC guidance</small>
        </div>

        <button
          onClick={() => setOpen(false)}
        >
          <X size={19} />
        </button>

      </div>

      <div className="chat-messages">

        {messages.map((msg, index) => (

          <div
            key={index}
            className={
              msg.role === "user"
                ? "chat-message user"
                : "chat-message assistant"
            }
          >
            {msg.text}
          </div>

        ))}

      </div>

      <div className="chat-input">

        <input
          value={message}
          onChange={(e) =>
            setMessage(e.target.value)
          }
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage();
            }
          }}
          placeholder="Ask about your CBC..."
        />

        <button onClick={sendMessage}>
          <Send size={18} />
        </button>

      </div>

      <div className="chat-disclaimer">
        Educational information only. Not a diagnosis.
      </div>

    </div>
  );
}