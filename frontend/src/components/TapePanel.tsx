type Props = {
  symbol: string | null;
};

export default function TapePanel({ symbol }: Props) {
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
        Time & Sales (Tape)
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
          maxHeight: "200px",
          overflowY: "auto",
        }}
      >
        Placeholder for Time & Sales stream.  
        Later: stream prints (price, size, side) in real time.
      </div>
    </div>
  );
}
