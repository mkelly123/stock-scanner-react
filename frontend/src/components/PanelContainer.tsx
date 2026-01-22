import React from "react";

interface Props {
  title: string;
  onMaximize: () => void;
  isMaximized: boolean;
  children: React.ReactNode;
}

export default function PanelContainer({
  title,
  onMaximize,
  isMaximized,
  children
}: Props) {
  return (
    <div className={`panel-container ${isMaximized ? "maximized" : ""}`}>
      <div className="panel-header">
        <span className="panel-title">{title}</span>
        <button className="panel-maximize-btn" onClick={onMaximize}>
          {isMaximized ? "Restore" : "Maximize"}
        </button>
      </div>

      <div className="panel-content">
        {children}
      </div>
    </div>
  );
}
