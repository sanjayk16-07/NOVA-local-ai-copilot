import { useEffect, useState } from "react";
import "./App.css";

type Message = {
  role: "user" | "nova";
  content: string;
  model?: string;
};

type ProjectFile = {
  path: string;
  content: string;
};

type Activity = {
  text: string;
  time: string;
};

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const [activePage, setActivePage] = useState<
    "chat" | "project" | "activity"
  >("chat");

  const [darkMode, setDarkMode] = useState(true);

  const [files, setFiles] = useState<ProjectFile[]>([]);
  const [selectedFile, setSelectedFile] =
    useState<ProjectFile | null>(null);

  const [activities, setActivities] = useState<Activity[]>([
    {
      text: "NOVA started successfully",
      time: "Now",
    },
    {
      text: "Ollama connected",
      time: "Now",
    },
    {
      text: "Watchdog monitoring project",
      time: "Now",
    },
    {
      text: "Privacy Gateway ready",
      time: "Now",
    },
  ]);

  const API_URL =
    import.meta.env.VITE_API_URL ||
    "http://127.0.0.1:8000";
   
  // Load project files
  useEffect(() => {
    const loadFiles = async () => {
      try {
        const response = await fetch(
          `${API_URL}/files`
        );

        if (!response.ok) {
          throw new Error("Failed to load files");
        }

        const data = await response.json();

        setFiles(data.files || []);
      } catch (error) {
        console.error("Could not load project files", error);
      }
    };

    loadFiles();
  }, [API_URL]);

  const addActivity = (text: string) => {
    setActivities((prev) => [
      {
        text,
        time: "Just now",
      },
      ...prev,
    ]);
  };

  const sendMessage = async () => {
    if (!query.trim() || loading) return;

    const currentQuery = query.trim();

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: currentQuery,
      },
    ]);

    setQuery("");
    setLoading(true);

    addActivity(`Processing: ${currentQuery}`);

    try {
      const response = await fetch(
        `${API_URL}/chat?query=${encodeURIComponent(
          currentQuery
        )}`
      );

      if (!response.ok) {
        throw new Error("Backend request failed");
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "nova",
          content: data.answer,
          model: data.model,
        },
      ]);

      addActivity(
        `Response generated using ${data.model}`
      );
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "nova",
          content:
            "I couldn't connect to the NOVA backend. Make sure FastAPI is running.",
        },
      ]);

      addActivity("Backend connection failed");
    } finally {
      setLoading(false);
    }
  };

  const openFile = (file: ProjectFile) => {
    setSelectedFile(file);

    addActivity(`Opened ${file.path}`);
  };

  return (
    <div
      className={`nova ${
        darkMode ? "dark" : "light"
      }`}
    >
      {/* SIDEBAR */}

      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">N</div>

          <div>
            <div className="brand-name">
              NOVA
            </div>

            <div className="brand-subtitle">
              Developer Intelligence
            </div>
          </div>
        </div>

        <div className="workspace-label">
          WORKSPACE
        </div>

        <nav>
          <button
            className={`nav-item ${
              activePage === "chat"
                ? "active"
                : ""
            }`}
            onClick={() => {
              setActivePage("chat");
              setSelectedFile(null);
            }}
          >
            <span>⌘</span>
            Chat
          </button>

          <button
            className={`nav-item ${
              activePage === "project"
                ? "active"
                : ""
            }`}
            onClick={() => {
              setActivePage("project");
              setSelectedFile(null);
            }}
          >
            <span>◫</span>
            Project
          </button>

          <button
            className={`nav-item ${
              activePage === "activity"
                ? "active"
                : ""
            }`}
            onClick={() => {
              setActivePage("activity");
              setSelectedFile(null);
            }}
          >
            <span>◌</span>
            Activity
          </button>
        </nav>

        {/* PROJECT FILES */}

        <div className="sidebar-section">
          <div className="workspace-label">
            PROJECT
          </div>

          <div className="project">
            <span className="folder">▾</span>
            sample-project
          </div>

          {files.map((file) => (
            <button
              className="file"
              key={file.path}
              onClick={() => openFile(file)}
            >
              <span>◇</span>
              {file.path}
            </button>
          ))}
        </div>

        {/* SYSTEM */}

        <div className="system-status">
          <div className="workspace-label">
            SYSTEM
          </div>

          <div className="system-row">
            <span className="online"></span>
            Ollama
            <span className="system-value">
              Local
            </span>
          </div>

          <div className="system-row">
            <span className="online"></span>
            Watchdog
            <span className="system-value">
              Active
            </span>
          </div>

          <div className="system-row">
            <span className="online"></span>
            Privacy
            <span className="system-value">
              Protected
            </span>
          </div>

          <div className="system-row">
            <span className="online"></span>
            Gemini
            <span className="system-value">
              Ready
            </span>
          </div>
        </div>

        <div className="sidebar-footer">
          <div className="security-icon">
            ◉
          </div>

          <div>
            <strong>Local-first</strong>

            <span>
              Your code stays yours.
            </span>
          </div>
        </div>
      </aside>

      {/* MAIN */}

      <main className="main">
        <header className="topbar">
          <div>
            <div className="page-title">
              {activePage === "chat" &&
                "NOVA Assistant"}

              {activePage === "project" &&
                "Project Explorer"}

              {activePage === "activity" &&
                "System Activity"}
            </div>

            <div className="page-subtitle">
              {activePage === "chat" &&
                "Project-aware developer intelligence"}

              {activePage === "project" &&
                "Explore your local project"}

              {activePage === "activity" &&
                "Monitor NOVA operations"}
            </div>
          </div>

          <div className="top-actions">
            <div className="connection">
              <span className="online"></span>
              System Online
            </div>

            {/* THEME BUTTON */}

            <button
              className="icon-button"
              onClick={() =>
                setDarkMode((prev) => !prev)
              }
              title={
                darkMode
                  ? "Switch to light mode"
                  : "Switch to dark mode"
              }
            >
              {darkMode ? "☀" : "☾"}
            </button>
          </div>
        </header>

        {/* CHAT PAGE */}

        {activePage === "chat" && (
          <>
            <section className="chat">
              {messages.length === 0 ? (
                <div className="welcome">
                  <div className="nova-orb">
                    <div>N</div>
                  </div>

                  <div className="welcome-tag">
                    NEAR-DEVICE OPTIMIZED VIRTUAL
                    ASSISTANT
                  </div>

                  <h1>
                    Build faster.
                    <br />
                    <span>
                      Keep your code private.
                    </span>
                  </h1>

                  <p>
                    NOVA understands your local
                    project and helps you reason
                    about your code without sending
                    raw source code to the cloud.
                  </p>

                  <div className="suggestions">
                    <button
                      onClick={() =>
                        setQuery(
                          "How does the calculate function work?"
                        )
                      }
                    >
                      <span>⌁</span>
                      Explain this project
                    </button>

                    <button
                      onClick={() =>
                        setQuery(
                          "Analyze the architecture of this project"
                        )
                      }
                    >
                      <span>◈</span>
                      Analyze architecture
                    </button>

                    <button
                      onClick={() =>
                        setQuery(
                          "Find potential improvements in this code"
                        )
                      }
                    >
                      <span>✦</span>
                      Improve my code
                    </button>
                  </div>
                </div>
              ) : (
                <div className="messages">
                  {messages.map(
                    (message, index) => (
                      <div
                        key={index}
                        className={`message ${message.role}`}
                      >
                        <div className="message-avatar">
                          {message.role ===
                          "user"
                            ? "U"
                            : "N"}
                        </div>

                        <div className="message-content">
                          <div className="message-header">
                            <strong>
                              {message.role ===
                              "user"
                                ? "You"
                                : "NOVA"}
                            </strong>

                            {message.model && (
                              <span className="model-badge">
                                {message.model ===
                                "qwen"
                                  ? "LOCAL · QWEN"
                                  : "CLOUD · GEMINI"}
                              </span>
                            )}
                          </div>

                          <div className="message-text">
                            {message.content}
                          </div>
                        </div>
                      </div>
                    )
                  )}

                  {loading && (
                    <div className="message nova">
                      <div className="message-avatar">
                        N
                      </div>

                      <div className="message-content">
                        <div className="message-header">
                          <strong>NOVA</strong>
                        </div>

                        <div className="thinking">
                          <span></span>
                          <span></span>
                          <span></span>
                          <em>Thinking...</em>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </section>

            {/* CHAT INPUT */}

            <div className="composer-wrapper">
              <div className="composer">
                <textarea
                  value={query}
                  onChange={(e) =>
                    setQuery(e.target.value)
                  }
                  onKeyDown={(e) => {
                    if (
                      e.key === "Enter" &&
                      !e.shiftKey
                    ) {
                      e.preventDefault();
                      sendMessage();
                    }
                  }}
                  placeholder="Ask NOVA about your code..."
                  rows={1}
                />

                <button
                  className="send-button"
                  onClick={sendMessage}
                  disabled={
                    !query.trim() || loading
                  }
                >
                  ↑
                </button>
              </div>

              <div className="composer-footer">
                <span>
                  Enter to send · Shift + Enter
                  for new line
                </span>

                <span>
                  🔒 Local-first AI
                </span>
              </div>
            </div>
          </>
        )}

        {/* PROJECT PAGE */}

        {activePage === "project" && (
          <section className="page-content">
            <div className="section-heading">
              <div>
                <h2>Project Files</h2>
                <p>
                  Files discovered by NOVA's local
                  file scanner.
                </p>
              </div>

              <div className="file-count">
                {files.length} files
              </div>
            </div>

            <div className="project-grid">
              <div className="file-list-card">
                {files.length === 0 ? (
                  <div className="empty-state">
                    No project files found.
                  </div>
                ) : (
                  files.map((file) => (
                    <button
                      key={file.path}
                      className={`project-file ${
                        selectedFile?.path ===
                        file.path
                          ? "selected"
                          : ""
                      }`}
                      onClick={() =>
                        openFile(file)
                      }
                    >
                      <span className="file-icon">
                        ◇
                      </span>

                      <span>
                        <strong>
                          {file.path}
                        </strong>

                        <small>
                          Local project file
                        </small>
                      </span>
                    </button>
                  ))
                )}
              </div>

              <div className="code-card">
                {selectedFile ? (
                  <>
                    <div className="code-header">
                      <span>
                        {selectedFile.path}
                      </span>

                      <span className="local-badge">
                        LOCAL
                      </span>
                    </div>

                    <pre>
                      <code>
                        {selectedFile.content}
                      </code>
                    </pre>
                  </>
                ) : (
                  <div className="empty-state">
                    Select a file to inspect it.
                  </div>
                )}
              </div>
            </div>
          </section>
        )}

        {/* ACTIVITY PAGE */}

        {activePage === "activity" && (
          <section className="page-content">
            <div className="section-heading">
              <div>
                <h2>NOVA Activity</h2>
                <p>
                  Recent operations performed by
                  the assistant.
                </p>
              </div>

              <div className="status-pill">
                <span className="online"></span>
                Live
              </div>
            </div>

            <div className="activity-card">
              {activities.map(
                (activity, index) => (
                  <div
                    className="activity-item"
                    key={index}
                  >
                    <div className="activity-dot">
                      <span></span>
                    </div>

                    <div className="activity-info">
                      <strong>
                        {activity.text}
                      </strong>

                      <small>
                        {activity.time}
                      </small>
                    </div>
                  </div>
                )
              )}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;