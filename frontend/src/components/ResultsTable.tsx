import type { ResultRow } from "../types";

type Props = {
  results: ResultRow[];
  onSelectSymbol: (symbol: string) => void;
  selectedSymbol: string | null;
};

export default function ResultsTable({
  results,
  onSelectSymbol,
  selectedSymbol,
}: Props) {
  if (results.length === 0) {
    return <div>No results found.</div>;
  }

  return (
    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr style={{ backgroundColor: "#333", color: "white" }}>
          <th style={{ padding: "8px" }}>Symbol</th>
          <th style={{ padding: "8px" }}>Score</th>
          <th style={{ padding: "8px" }}>Volume</th>
          <th style={{ padding: "8px" }}>Price</th>
          <th style={{ padding: "8px" }}>Trend</th>
        </tr>
      </thead>
      <tbody>
        {results.map((row) => (
          <tr
            key={row.symbol}
            onClick={() => onSelectSymbol(row.symbol)}
            style={{
              backgroundColor:
                row.symbol === selectedSymbol ? "#444" : "transparent",
              cursor: "pointer",
            }}
            // onClick={() => onSelectSymbol(row.symbol)}
          >
            <td style={{ padding: "8px" }}>{row.symbol}</td>
            <td style={{ padding: "8px" }}>{row.score}</td>
            <td style={{ padding: "8px" }}>{row.volume.toLocaleString()}</td>
            <td style={{ padding: "8px" }}>${row.price.toFixed(2)}</td>
            <td style={{ padding: "8px" }}>{row.trend}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
