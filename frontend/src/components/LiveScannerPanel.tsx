import { useEffect, useState } from "react";

type ScanResult = {
  symbol: string;
  price: number;
  volume: number;
  float: number;
  relVolume: number;
  changePct: number;
};

export default function LiveScannerPanel() {
  const [signals, setSignals] = useState<ScanResult[]>([]);
  const [live, setLive] = useState(false);

  useEffect(() => {
    if (!live) return;

    const ws = new WebSocket("ws://localhost:8000/api/ws/scan");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setSignals(data);
    };

    ws.onerror = () => {
      console.error("WebSocket error");
    };

    return () => ws.close();
  }, [live]);

  return (
    <div>
      <button onClick={() => setLive((v) => !v)}>
        {live ? "Stop Live Mode" : "Start Live Mode"}
      </button>

      <table>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Price</th>
            <th>Volume</th>
            <th>Float</th>
            <th>Rel Vol</th>
            <th>Change %</th>
          </tr>
        </thead>
        <tbody>
          {signals.map((s) => (
            <tr key={s.symbol}>
              <td>{s.symbol}</td>
              <td>{s.price}</td>
              <td>{s.volume.toLocaleString()}</td>
              <td>{s.float.toLocaleString()}</td>
              <td>{s.relVolume}</td>
              <td>{s.changePct}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
