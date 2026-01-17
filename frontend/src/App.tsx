import { useState } from "react";
import { Responsive as ResponsiveGridLayout } from "react-grid-layout";
import type { ResponsiveProps } from "react-grid-layout";

import PanelContainer from "./components/PanelContainer";
import ScannerPanel from "./components/ScannerPanel";
import ChartPanel from "./components/ChartPanel";
import Level2Panel from "./components/Level2Panel";
import TapePanel from "./components/TapePanel";
import NewsPanel from "./components/NewsPanel";
import type { ResultRow } from "./types";

import "react-grid-layout/css/styles.css";
import "react-resizable/css/styles.css";
import "./index.css";

export default function App() {
  const [maximizedPanel, setMaximizedPanel] = useState<string | null>(null);
  const [results, setResults] = useState<ResultRow[]>([]);
  const [selectedSymbol, setSelectedSymbol] = useState<string | null>(null);

  const handleSelectSymbol = (symbol: string) => {
    setSelectedSymbol(symbol);
  };

  // 🔥 Forced LG layout only — always 3 columns
  const layouts = {
    lg: [
      { i: "scanner", x: 0, y: 0, w: 3, h: 2 },
      { i: "chart",   x: 0, y: 2, w: 2, h: 3 },
      { i: "level2",  x: 2, y: 2, w: 1, h: 2 },
      { i: "tape",    x: 2, y: 4, w: 1, h: 2 },
      { i: "news",    x: 0, y: 5, w: 3, h: 2 }
    ]
  };

  const handleScan = async () => {
    try {
      const res = await fetch("http://localhost:8000/scan");
      const data = await res.json();
      setResults(data);
      setSelectedSymbol(null);
    } catch (err) {
      console.error("Scan failed:", err);
    }
  };

  const handleSample = () => {
    setResults([
      { symbol: "BACK", price: 6.35, volume: 485590, float: 1020000, relVolume: 3.35, changePct: 82.21 },
      { symbol: "BRFH", price: 1.52, volume: 39800000, float: 6890000, relVolume: 8598.03, changePct: 47.57 },
      { symbol: "PCSA", price: 2.38, volume: 67680000, float: 2230000, relVolume: 273.83, changePct: 47.22 },
      { symbol: "MNY",  price: 2.42, volume: 6870000,  float: 13820000, relVolume: 34.34, changePct: 34.44 },
      { symbol: "YYGH", price: 2.94, volume: 18040000, float: 34800000, relVolume: 41.26, changePct: 30.08 },
      { symbol: "POAI", price: 1.72, volume: 157690,  float: 3920000,  relVolume: 5.0,  changePct: 28.33 }
    ]);
  };

  return (
    <div style={{ width: "100%", height: "100%" }}>
      <ResponsiveGridLayout
        className="layout"
        layouts={{ lg: layouts.lg }}
        breakpoints={{ lg: 0 }}
        cols={{ lg: 3 }}
        rowHeight={140}
        draggableCancel=".no-drag"
      >
        <div key="scanner">
          <PanelContainer
            title="Scanner"
            onMaximize={() =>
              setMaximizedPanel(maximizedPanel === "scanner" ? null : "scanner")
            }
            isMaximized={maximizedPanel === "scanner"}
          >
            <ScannerPanel
              results={results}
              onScan={handleScan}
              onSample={handleSample}
              onSelectSymbol={handleSelectSymbol}
              selectedSymbol={selectedSymbol}
            />
          </PanelContainer>
        </div>

        <div key="chart">
          <PanelContainer
            title="Chart"
            onMaximize={() =>
              setMaximizedPanel(maximizedPanel === "chart" ? null : "chart")
            }
            isMaximized={maximizedPanel === "chart"}
          >
            <ChartPanel symbol={selectedSymbol} />
          </PanelContainer>
        </div>

        <div key="level2">
          <PanelContainer
            title="Level 2"
            onMaximize={() =>
              setMaximizedPanel(maximizedPanel === "level2" ? null : "level2")
            }
            isMaximized={maximizedPanel === "level2"}
          >
            <Level2Panel symbol={selectedSymbol} />
          </PanelContainer>
        </div>

        <div key="tape">
          <PanelContainer
            title="Time & Sales"
            onMaximize={() =>
              setMaximizedPanel(maximizedPanel === "tape" ? null : "tape")
            }
            isMaximized={maximizedPanel === "tape"}
          >
            <TapePanel symbol={selectedSymbol} />
          </PanelContainer>
        </div>

        <div key="news">
          <PanelContainer
            title="News"
            onMaximize={() =>
              setMaximizedPanel(maximizedPanel === "news" ? null : "news")
            }
            isMaximized={maximizedPanel === "news"}
          >
            <NewsPanel symbol={selectedSymbol} />
          </PanelContainer>
        </div>
      </ResponsiveGridLayout>
    </div>
  );
}
