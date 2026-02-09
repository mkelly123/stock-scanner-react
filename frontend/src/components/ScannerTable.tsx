import React from "react";
import type { ScannerResult } from "./LiveScannerPanel";

interface Props {
  data: ScannerResult[];
}

function ScoreBar({ value, max = 10 }: { value: number; max?: number }) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));

  return (
    <div style={{ width: "100%", background: "#222", height: 8, borderRadius: 4 }}>
      <div
        style={{
          width: `${pct}%`,
          height: "100%",
          background: pct > 70 ? "#4caf50" : pct > 40 ? "#ff9800" : "#f44336",
          borderRadius: 4,
          transition: "width 0.3s ease"
        }}
      />
    </div>
  );
}

export default function ScannerTable({ data }: Props) {
  return (
    <>
      <div style={{ color: "#888", marginBottom: 8 }}>
        Showing {data.length} results
      </div>

      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
        <thead>
          <tr style={{ textAlign: "left", borderBottom: "1px solid #444" }}>
            <th style={{ padding: "8px" }}>Symbol</th>
            <th style={{ padding: "8px" }}>Price</th>
            <th style={{ padding: "8px" }}>Swing Score</th>
            <th style={{ padding: "8px" }}>Trend</th>
            <th style={{ padding: "8px" }}>Breakout</th>
            <th style={{ padding: "8px" }}>Combined</th>
          </tr>
        </thead>

        <tbody>
          {data.map((row) => {
            const trendColor =
              row.trend === "uptrend"
                ? "rgba(0, 200, 0, 0.15)"
                : row.trend === "downtrend"
                ? "rgba(200, 0, 0, 0.15)"
                : "rgba(255, 255, 255, 0.05)";

            return (
              <tr key={row.symbol} style={{ background: trendColor }}>
                <td style={{ padding: "8px", fontWeight: 600 }}>{row.symbol}</td>
                <td style={{ padding: "8px" }}>{(row.price ?? 0).toFixed(2)}</td>

                <td style={{ padding: "8px", width: 120 }}>
                  <ScoreBar value={row.swingScore ?? 0} max={10} />
                </td>

                <td style={{ padding: "8px" }}>{row.trend ?? "—"}</td>

                <td style={{ padding: "8px" }}>
                  {row.breakout ? "🔥 Yes" : "—"}
                </td>

                <td style={{ padding: "8px", width: 120 }}>
                  <ScoreBar value={row.combinedScore ?? 0} max={10} />
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </>
  );
}
