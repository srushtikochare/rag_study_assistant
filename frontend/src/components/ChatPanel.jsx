import { useState } from "react";
import { evaluateAnswer } from "../api";

export default function ChatPanel() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await evaluateAnswer(question);
      setResult(res.data);
    } catch (err) {
      setResult({
        answer: "Oops! We couldn't process your question right now. Please try again.",
        sources: []
      });
    }

    setLoading(false);
  };

  const score = result?.evaluation?.score;
  const isGrounded = result?.evaluation?.grounded;

  return (
    <section className="notebook-section sticky-card">
      <h2>Ask a question</h2>

      <p className="section-hint">
        Grounded in the notes you've added above.
      </p>

      <div className="ask-row">
        <input
          className="ask-input"
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. What is generative AI?"
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
        />

        <button
          className="btn-primary"
          onClick={handleAsk}
          disabled={loading}
        >
          {loading ? (
            <span className="thinking-dots">
              <span />
              <span />
              <span />
            </span>
          ) : (
            <>
              Ask
              <svg
                width="13"
                height="13"
                viewBox="0 0 24 24"
                fill="none"
              >
                <path
                  d="M5 12h14M13 6l6 6-6 6"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </>
          )}
        </button>
      </div>

      {result && (
        <div className="answer-block">
          <div className="answer-label-row">
            <span className="answer-label">Answer</span>

            {score !== undefined && score !== null && (
              <span
                className={`stamp ${
                  isGrounded ? "grounded" : "ungrounded"
                }`}
              >
                {isGrounded ? "grounded" : "check sources"} · {score}/100
              </span>
            )}
          </div>

          <div className="answer-highlight">
            <p className="answer-text">{result.answer}</p>
          </div>

          {result.sources?.length > 0 && (
            <>
              <p className="sources-label">Sources</p>

              <ul className="doc-tags">
                {result.sources.map((s) => (
                  <li key={s} className="doc-tag">
                    {s}
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </section>
  );
}