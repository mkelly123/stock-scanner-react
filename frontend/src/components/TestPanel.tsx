import React from "react";

type PanelProps = {
  title: string;
  children: React.ReactNode;
  isMaximized?: boolean;
  onMaximize?: () => void;
  onClose?: () => void;
};

export default function TestPanel({
  title,
  children,
  isMaximized = false,
  onMaximize,
  onClose,
}: PanelProps) {
  return (
    <div
      style={{
        border: "1px solid var(--border)",
        borderRadius: "var(--radius)",
        background: "var(--panel)",
        boxShadow: "var(--shadow)",
        height: isMaximized ? "calc(100vh - 80px)" : "auto",
        width: "100%",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Header */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "8px 12px",
          borderBottom: "1px solid var(--border)",
          background: "var(--panel-header)",
          fontWeight: 600,
          userSelect: "none",
        }}
      >
        <span>{title}</span>

        <div style={{ display: "flex", gap: "8px" }}>
          {onMaximize && (
            <button
              onClick={onMaximize}
              style={{
                background: "transparent",
                border: "none",
                cursor: "pointer",
                fontSize: "16px",
              }}
            >
              ⛶
            </button>
          )}

          {onClose && (
            <button
              onClick={onClose}
              style={{
                background: "transparent",
                border: "none",
                cursor: "pointer",
                fontSize: "16px",
              }}
            >
              ✕
            </button>
          )}
        </div>
      </div>

      {/* Content */}
      <div style={{ padding: "12px", flex: 1 }}>{children}</div>
    </div>
  );
}
