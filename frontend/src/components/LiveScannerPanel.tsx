console.log("🔥 USING THIS FILE 🔥");

import React, { useEffect, useState } from "react";

type ScanResult = {
  symbol: string;
  price: number;
  volume: number;
  float: number;
  relVolume: number;
  changePct: number;
  score: number;
  flash?: boolean;
  highlight?: boolean;
};

export default function LiveScannerPanel() {
  const [signals, setSignals] = useState<ScanResult[]>([]);
  const [live, setLive] = useState(false);

  useEffect(() => {
    console.log("LiveScannerPanel LOADED");

    if (!live) return;

    console.log("Creating WebSocket…");
    const socket = new WebSocket("ws://localhost:8000/ws/scan");


    socket.onopen = () => {
      console.log("WS OPEN");
    };

    socket.onmessage = (event) => {
      console.log("WS MSG", event.data);

      const msg = JSON.parse(event.data);

      if (msg.type === "scanner_update") {
        const row: ScanResult = msg.data;

        setSignals((prev) => {
          const highlight = row.volume > 50_000_000;
          const enrichedRow = { ...row, flash: true, highlight };

          const idx = prev.findIndex((s) => s.symbol === row.symbol);

          if (idx >= 0) {
            const updated = [...prev];
            updated[idx] = enrichedRow;
            return updated;
          }

          return [...prev, enrichedRow];
        });
      }
    };

    socket.onerror = (event) => {
      console.log("WS ERR", event);
    };

    socket.onclose = () => {
      console.log("WS CLOSE");
    };

    return () => {
      console.log("Closing WebSocket…");
      socket.close();
    };
  }, [live]);

  return (
    <div className="scanner-container">
      <button className="live-btn" onClick={() => setLive((v) => !v)}>
        {live ? "Stop Live Mode" : "Start Live Mode"}
      </button>

      <table className="scanner-table">
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Price</th>
            <th>Volume</th>
            <th>Float</th>
            <th>Rel Vol</th>
            <th>Change %</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {signals.map((s) => (
            <tr
              key={s.symbol}
              className={`${s.flash ? "flash" : ""} ${s.highlight ? "highlight" : ""}`}
            >
              <td>{s.symbol}</td>
              <td>{s.price}</td>
              <td>{s.volume.toLocaleString()}</td>
              <td>{s.float.toLocaleString()}</td>
              <td className={s.relVolume >= 1 ? "positive" : "negative"}>
                {s.relVolume.toFixed(2)}
              </td>
              <td className={s.changePct >= 0 ? "positive" : "negative"}>
                {s.changePct.toFixed(2)}%
              </td>
              <td>{s.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
