// type Props = {
//   symbol: string | null;
// };

// export default function ChartPanel({ symbol }: Props) {
//   return (
//     <div
//       style={{
//         minHeight: "260px",
//         borderRadius: "var(--radius)",
//         border: "1px dashed var(--border)",
//         display: "flex",
//         flexDirection: "column",
//         padding: "12px",
//         gap: "8px",
//       }}
//     >
//       <div
//         style={{
//           display: "flex",
//           justifyContent: "space-between",
//           alignItems: "center",
//         }}
//       >
//         <h2 style={{ margin: 0, fontSize: "16px" }}>Chart</h2>
//         <span style={{ color: "var(--text-muted)", fontSize: "14px" }}>
//           {symbol ?? "No symbol selected"}
//         </span>
//       </div>
//       <div
//         style={{
//           flex: 1,
//           borderRadius: "6px",
//           border: "1px dashed var(--border)",
//           display: "flex",
//           flexDirection: "column",
//           alignItems: "center",
//           justifyContent: "center",
//           color: "var(--text-muted)",
//           fontSize: "14px",
//         }}
//       >
//         Chart placeholder — TradingView / lightweight-charts goes here.
//       </div>
//     </div>
//   );
// }



export default function ChartPanel({ symbol }: { symbol: string | null }) {
  return (
    <div
      style={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        padding: "12px",
        gap: "8px",
        borderRadius: "var(--radius)",
        border: "1px dashed var(--border)",
      }}
    >
      <div style={{ fontWeight: 600 }}>Chart</div>
      {!symbol ? (
        <div style={{ color: "var(--text-muted)" }}>
          No symbol selected<br />
          <br />
          Chart placeholder — TradingView / lightweight-charts goes here.
        </div>
      ) : (
        <div>Chart for {symbol}</div>
      )}
    </div>
  );
}
