import { useState } from "react";
import type { ResultRow } from "../App";

type Props = { 
  results: ResultRow[]; 
  onSelectSymbol: (symbol: string) => void; 
  selectedSymbol: string | null; 
};

export default function ResultsTable({ results }: Props) {
  const [sortKey, setSortKey] = useState<keyof ResultRow>("score");
  const [sortDir, setSortDir] = useState<"asc" | "desc">("desc");

  if (!results || results.length === 0) { 
    return <div>No results found.</div>; 
  }
console.log("ResultsTable received:", results);

  const sorted = [...results].sort((a, b) => {
    const valA = a[sortKey] ?? 0;
    const valB = b[sortKey] ?? 0;

    if (sortDir === "asc") return valA > valB ? 1 : -1;
    return valA < valB ? 1 : -1;
  });

  const toggleSort = (key: keyof ResultRow) => {
    if (sortKey === key) {
      setSortDir(sortDir === "asc" ? "desc" : "asc");
    } else {
      setSortKey(key);
      setSortDir("desc");
    }
  };

  const renderSparkline = (history?: number[]) => {
    if (!history || history.length === 0) return null;

    const max = Math.max(...history);
    const min = Math.min(...history);

    return (
      <svg width="80" height="24">
        {history.map((v, i) => {
          const x = (i / (history.length - 1)) * 80;
          const y = 24 - ((v - min) / (max - min)) * 24;
          return <circle key={i} cx={x} cy={y} r={1.5} fill="blue" />;
        })}
      </svg>
    );
  };

  return (
    <table className="table" style={{ width: "100%", marginTop: "1rem", borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <th onClick={() => toggleSort("symbol")}>Symbol</th>
          <th onClick={() => toggleSort("price")}>Price</th>
          <th onClick={() => toggleSort("volume")}>Volume</th>
          <th onClick={() => toggleSort("score")}>Score</th>
          <th onClick={() => toggleSort("trend")}>Trend</th>
          <th>Sparkline</th>
        </tr>
      </thead>

      <tbody>
        {sorted.map((row, i) => (
          <tr
            key={i}
            style={{
              background: row.score > 80 ? "#e8ffe8" : row.score < 40 ? "#ffe8e8" : "white",
            }}
          >
            <td>{row.symbol}</td>
            <td>${row.price.toFixed(2)}</td>
            <td>{row.volume.toLocaleString()}</td>

            <td
              style={{
                fontWeight: "bold",
                color: row.score > 80 ? "green" : row.score < 40 ? "red" : "black",
              }}
            >
              {row.score}
            </td>

            <td>
              {row.trend}{" "}
              {row.trend.toLowerCase().includes("up") ? "▲" : row.trend.toLowerCase().includes("down") ? "▼" : ""}
            </td>

            <td>{renderSparkline(row.history)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
