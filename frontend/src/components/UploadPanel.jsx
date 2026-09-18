import { useState } from "react";
import { uploadPDF, getDocuments } from "../api";

export default function UploadPanel() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [docs, setDocs] = useState([]);

  const handleUpload = async () => {
    if (!file) return;
    setStatus("Reading and indexing your notes...");
    try {
      const res = await uploadPDF(file);
      setStatus(`Added ${res.data.chunks_added} sections from ${res.data.filename}`);
      const docsRes = await getDocuments();
      setDocs(docsRes.data.documents);
      setFile(null);
    } catch (err) {
      setStatus("Couldn't reach the backend — check it's running.");
    }
  };

  return (
    <section className="notebook-section index-card">
      <h2>Your notes</h2>
      <p className="section-hint">Add a PDF once, then ask it anything.</p>

      <div className="upload-row">
        <label className="file-input">
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
            <path d="M21.44 11.05l-9.19 9.19a5 5 0 01-7.07-7.07l9.19-9.19a3.5 3.5 0 014.95 4.95l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <span>{file ? file.name : "Choose a PDF"}</span>
        </label>
        <button className="btn-primary" onClick={handleUpload} disabled={!file}>
          Add to notes
        </button>
      </div>

      <p className="status-line">{status}</p>

      {docs.length > 0 && (
        <ul className="doc-tags">
          {docs.map((d) => (
            <li key={d} className="doc-tag">{d}</li>
          ))}
        </ul>
      )}
    </section>
  );
}