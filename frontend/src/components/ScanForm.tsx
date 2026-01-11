import { useState } from "react";

type Props = {
  onScan: (mode: string, universe: string) => void;
};

export default function ScanForm({ onScan }: Props) {
  const [mode, setMode] = useState("stocks");
  const [universe, setUniverse] = useState("sp500");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onScan(mode, universe);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Scan Settings</h2>

      <label>
        Mode:
        <select value={mode} onChange={(e) => setMode(e.target.value)}>
          <option value="stocks">Stocks</option>
          <option value="etfs">ETFs</option>
        </select>
      </label>

      <label>
        Universe:
        <select value={universe} onChange={(e) => setUniverse(e.target.value)}>
          <option value="sp500">S&P 500</option>
          <option value="nasdaq">Nasdaq 100</option>
          <option value="custom">Custom Watchlist</option>
        </select>
      </label>

      <button className="button-primary">Run Scan</button>
    </form>
  );
}
