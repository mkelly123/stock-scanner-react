import { useEffect } from "react";
import { FaWindowMaximize, FaWindowRestore, FaTimes } from "react-icons/fa";

type PanelProps = {
  title: string;
  children: React.ReactNode;
  isMaximized?: boolean;
  onMaximize?: () => void;
  onClose?: () => void;
};

export default function PanelContainer({
  title,
  children,
  isMaximized = false,
  onMaximize,
  onClose,
}: PanelProps) {
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isMaximized && onMaximize) {
        onMaximize();
      }
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [isMaximized, onMaximize]);

  return (
    <div
      style={{
        background: "var(--panel)",
        color: "white",
        margin: isMaximized ? "0" : "8px 0",
        position: isMaximized ? "fixed" : "relative",
        top: isMaximized ? 0 : "auto",
        left: isMaximized ? 0 : "auto",
        width: isMaximized ? "100vw" : "100%",
        height: isMaximized ? "100vh" : "100%",
        minHeight: "100%",
        display: "flex",
        flexDirection: "column",
        borderRadius: "var(--radius)",
        boxShadow: "var(--shadow)",
        border: "1px solid var(--border)",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          background: "#2f2f2f",
          padding: "8px 12px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          position: "sticky",
          top: 0,
          zIndex: 1000,
          cursor: "pointer",
          borderRadius: "var(--radius)",
        }}
        onDoubleClick={onMaximize}
      >
        <span style={{ fontWeight: 600 }}>{title}</span>
        <div style={{ display: "flex", gap: "8px" }}>
          {onMaximize && (
            <button onClick={onMaximize}>
              {isMaximized ? <FaWindowRestore /> : <FaWindowMaximize />}
            </button>
          )}
          {onClose && (
            <button onClick={onClose}>
              <FaTimes />
            </button>
          )}
        </div>
      </div>

      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          padding: "12px",
          overflow: "auto",
        }}
      >
        {children}
      </div>
    </div>
  );
}
