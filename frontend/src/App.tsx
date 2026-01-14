console.log("PanelContainer loaded");

import { useState } from "react";
import "./index.css";

import ScannerPanel from "./components/ScannerPanel";
import ChartPanel from "./components/ChartPanel";
import Level2Panel from "./components/Level2Panel";
import TapePanel from "./components/TapePanel";
import TestPanel from "./components/TestPanel.tsx";
import PanelContainer from "./components/PanelContainer.tsx";
import { usePanels } from "./components/state/usePanels";

export type ResultRow = {
  symbol: string;
  score: number;
  volume: number;
  price: number;
  trend: string;
  history?: number[];
};

export default function App() {
  const [results, setResults] = useState<ResultRow[]>([]);
  const [selectedSymbol, setSelectedSymbol] = useState<string | null>(null);
 
  const {
    // visiblePanels,
    maximizedPanel,
    hidePanel,
    toggleMaximize,
  } = usePanels();


  const handleScan = async () => {
    const res = await fetch("/api/scan?mode=stocks&universe=AAPL,MSFT,TSLA");
    const data: ResultRow[] = await res.json();
    setResults(data);
    if (data.length > 0) {
      setSelectedSymbol(data[0].symbol);
    }
  };

  const loadSampleData = () => {
    const sample: ResultRow[] = [
      {
        symbol: "NVDA",
        price: 542.19,
        volume: 31200000,
        score: 84,
        trend: "Strong Uptrend",
        history: [520, 525, 530, 540, 545, 542],
      },
      {
        symbol: "TSLA",
        price: 212.55,
        volume: 40800000,
        score: 72,
        trend: "Recovering",
      },
      {
        symbol: "AAPL",
        price: 189.44,
        volume: 51200000,
        score: 65,
        trend: "Sideways",
      },
      {
        symbol: "AMD",
        price: 162.88,
        volume: 41000000,
        score: 88,
        trend: "Uptrend",
      },
    ];
    setResults(sample);
    setSelectedSymbol(sample[0].symbol);
  };

  return (
    <div
      style={{
        maxWidth: "1600px",
        margin: "0 auto",
        padding: "24px",
      }}
    >
      <h1
        style={{
          fontSize: "28px",
          fontWeight: 700,
          marginBottom: "20px",
        }}
      >
        Momentum Breakout Workstation
      </h1>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1.3fr 2fr 1.2fr",
          gap: "20px",
          alignItems: "start",
        }}
      >
        {/* Left column: Scanner */}
        <ScannerPanel
          results={results}
          onScan={handleScan}
          onSample={loadSampleData}
          onSelectSymbol={setSelectedSymbol}
          selectedSymbol={selectedSymbol}
        />

        {/* Middle column: Chart */}
        {/* <PanelContainer
          title="Chart"
          isMaximized={maximizedPanel === "chart"}
          onMaximize={() => toggleMaximize("chart")}
          onClose={() => hidePanel("chart")}
        >
          <ChartPanel symbol={selectedSymbol} />
        </PanelContainer> */}

<TestPanel
 title="Chart"
          isMaximized={maximizedPanel === "chart"}
        >  
        
          <ChartPanel symbol={selectedSymbol} />
</TestPanel>
         
        

        
        {/* Right column: Level 2 + Tape */}
        <div>
          <Level2Panel symbol={selectedSymbol} />
          <div style={{ height: "16px" }} />
          <TapePanel symbol={selectedSymbol} />
        </div>
      </div>
    </div>
  );
}
