console.log(">>> ACTIVE APP.TSX LOADED <<<");



import { useState } from "react";
import ScanForm from "./components/ScanForm";
import ResultsTable from "./components/ResultsTable";

export type ScanResult = {
  symbol: string;
  date: string;
  price: number;
  pct_change: number;
  volume: number;
  score: number;
  mode: string;
};

export default function App() {
  const [results, setResults] = useState<ScanResult[]>([]);

  const handleDummyLoad = () => {
    setResults([
      {
        symbol: "AAPL",
        date: "2026-01-10",
        price: 172.34,
        pct_change: 2.1,
        volume: 100000,
        score: 87,
        mode: "stocks",
      },
    ]);
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Momentum Breakout Scanner</h1>
      <ScanForm onScan={() => {}} />
      <button onClick={handleDummyLoad}>Load Dummy Data</button>
      {results.length > 0 && <ResultsTable data={results} />}
    </div>
  );
}
