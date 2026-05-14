import React, { useState, useEffect } from "react";

export default function Chatbot() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const API_URL = "http://localhost:8000/chat";

  const askQuestion = async () => {
    if (!question) return;

    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: question,
        selected_text: "",
      }),
    });

    const data = await res.json();
    setAnswer(data.answer);
  };

  return (
    <div style={{ marginTop: "20px" }}>
      <h3>Ask AI 🤖</h3>

      <input
        type="text"
        placeholder="Ask something..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{ padding: "10px", width: "300px" }}
      />

      <br /><br />

      <button onClick={askQuestion}>
        Ask
      </button>

      <p><strong>Answer:</strong> {answer}</p>
    </div>
  );
}