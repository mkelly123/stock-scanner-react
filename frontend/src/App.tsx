import { useState } from "react";
import ScanForm from "./components/ScanForm";
import ResultsTable from "./components/ResultsTable";

type ResultRow = {
  symbol: string;
  price: number;
  volume: number;
  score: number;
  trend: string;
  history?: number[];
};

export default function App() {
  const [results, setResults] = useState<ResultRow[]>([]);

  const handleScan = async (mode: string, universe: string) => {
    console.log("Scanning:", { mode, universe });

    // Replace with actual backend call
     const response = await fetch(`/api/scan?mode=${mode}&universe=${universe}`);
    //const response = await fetch(`/scan?mode=${mode}&universe=${universe}`);
    const data = await response.json();

    setResults(data);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>Momentum Breakout Scanner</h1>

      <ScanForm onScan={handleScan} />

      <button
        style={{ marginTop: "1rem" }}
        onClick={() =>
          setResults([
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
              history: [190, 195, 200, 205, 210, 212],
            },
            {
              symbol: "AAPL",
              price: 189.44,
              volume: 51200000,
              score: 65,
              trend: "Sideways",
              history: [188, 189, 190, 189, 188, 189],
            },
            {
              symbol: "AMD",
              price: 162.88,
              volume: 41000000,
              score: 88,
              trend: "Uptrend",
              history: [150, 152, 155, 158, 160, 162],
            },
          ])
        }
      >
        Load Realistic Sample Data
      </button>

      <ResultsTable results={results} />
    </div>
  );
}
