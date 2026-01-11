type Props = {
  symbol: string | null;
};

export default function Level2Panel({ symbol }: Props) {
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
      <h2 style={{ marginTop: 0, fontSize: "18px", marginBottom: "8px" }}>
        Level 2 Order Book
      </h2>
      <div style={{ color: "var(--text-muted)", fontSize: "14px", marginBottom: "8px" }}>
        {symbol ? `Symbol: ${symbol}` : "No symbol selected"}
      </div>

      <div
        style={{
          borderRadius: "6px",
          border: "1px dashed var(--border)",
          padding: "12px",
          color: "var(--text-muted)",
          fontSize: "13px",
        }}
      >
        Placeholder for Level 2 data (bids/asks, depth, ladders).  
        Later: subscribe to a Level 2 WebSocket feed here.
      </div>
    </div>
  );
}
