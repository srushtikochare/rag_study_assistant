import UploadPanel from "./components/UploadPanel";
import ChatPanel from "./components/ChatPanel";

function SectionDivider() {
  return (
    <div className="section-divider">
      <span className="line" />
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M8 1v14M1 8h14" stroke="currentColor" strokeWidth="1" strokeLinecap="round" transform="rotate(45 8 8)" />
      </svg>
      <span className="line" />
    </div>
  );
}

function App() {
  return (
    <div className="desk">
      <div className="page-wrap">
        <div className="page">
          <div className="torn-edge" />
          <div className="tape tape-left" />
          <div className="tape tape-right" />

          <header className="site-header">
            <div className="badge-icon">
              <svg width="30" height="30" viewBox="0 0 24 24" fill="none">
                <path d="M4 19.5A2.5 2.5 0 016.5 17H20V4H6.5A2.5 2.5 0 004 6.5v13z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round" />
                <path d="M4 19.5A2.5 2.5 0 016.5 22H20" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            <h1>
              RAG Study Assistant
              <svg className="underline-squiggle" width="220" height="10" viewBox="0 0 220 10" fill="none">
                <path d="M2 7C20 2 38 2 56 6C74 10 92 3 110 3C128 3 146 9 164 6C182 3 200 2 218 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              </svg>
            </h1>
            <p className="tagline">
              Ask your notes anything. Answers stay grounded in what you
              actually uploaded — cited, not guessed.
            </p>
          </header>

          <UploadPanel />
          <SectionDivider />
          <ChatPanel />
        </div>
      </div>
    </div>
  );
}

export default App;