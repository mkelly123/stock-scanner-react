// Required for React 16 JSX transform
import React from "react";
import DockviewWrapper from "./layout/DockviewWrapper";

export default function App() {
  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <DockviewWrapper />
    </div>
  );
}
