import ResultsTable from "./ResultsTable";
import type { ResultRow } from "../types";

type Props = {
  results: ResultRow[];
  onScan: () => void;
  onSample: () => void;
  onSelectSymbol: (symbol: string) => void;
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
    <div>
      <div style={{ display: "flex", gap: "12px", marginBottom: "12px", minHeight: "320px" }}>
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
