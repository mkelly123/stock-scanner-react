import React, { useState } from "react";
import type { ReactNode } from "react";

interface TabConfig {
  label: string;
  content: ReactNode | (() => ReactNode);
}

interface TabsProps {
  tabs: TabConfig[];
}

export default function Tabs({ tabs }: TabsProps) {
  const [active, setActive] = useState<number>(0);

  return (
    <div style={{ width: "100%", height: "100%" }}>
      <div style={{ display: "flex", borderBottom: "1px solid #333" }}>
        {tabs.map((tab: TabConfig, i: number) => (
          <div
            key={i}
            onClick={() => setActive(i)}
            style={{
              padding: "8px 16px",
              cursor: "pointer",
              borderBottom:
                active === i ? "2px solid #4da3ff" : "2px solid transparent",
              color: active === i ? "#4da3ff" : "#ccc"
            }}
          >
            {tab.label}
          </div>
        ))}
      </div>

      <div style={{ padding: 10 }}>
        {typeof tabs[active].content === "function"
            ? (tabs[active].content as () => ReactNode)()
            : tabs[active].content}
      </div>
    </div>
  );
}
