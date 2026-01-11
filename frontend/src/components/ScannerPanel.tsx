import type { ResultRow } from "../App";
import ResultsTable from "./ResultsTable";

type Props = {
  results: ResultRow[];
  onScan: () => void;
  onSample: () => void;
  onSelectSymbol: (symbol: string | null) => void;
  selectedSymbol: string | null;
};

export default function ScannerPanel({
  results,
  onScan,
  onSample,
  onSelectSymbol,
  selectedSymbol,
}: Props) {
  return (
    <div
      style={{
        background: "var(--panel)",
        padding: "20px",
        borderRadius: "var(--radius)",
        boxShadow: "var(--shadow)",
        border: "1px solid var(--border)",
      }}
    >
      <div
        style={{
          display: "flex",
          gap: "12px",
          marginBottom: "16px",
          alignItems: "center",
        }}
      >
        <button className="button-primary" onClick={onScan}>
          Run Scan
        </button>

        <button className="button-secondary" onClick={onSample}>
          Load Realistic Sample Data
        </button>
      </div>

      <ResultsTable
        results={results}
        onSelectSymbol={onSelectSymbol}
        selectedSymbol={selectedSymbol}
      />
    </div>
  );
}
