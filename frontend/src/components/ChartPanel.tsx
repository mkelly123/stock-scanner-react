type Props = {
  symbol: string | null;
};

export default function ChartPanel({ symbol }: Props) {
  return (
    <div>
      <h2>Chart</h2>
      <div>{symbol ? `Symbol: ${symbol}` : "No symbol selected"}</div>
      {/* Chart rendering will go here */}
    </div>
  );
}



// type Props = {
//   selectedSymbol: string | null;
// };

// export default function ChartPanel({ selectedSymbol }: Props) {
//   return (
//     <div
//       style={{
//         background: "var(--panel)",
//         padding: "20px",
//         borderRadius: "var(--radius)",
//         boxShadow: "var(--shadow)",
//         border: "1px solid var(--border)",
//         minHeight: "320px",
//       }}
//     >
//       <div
//         style={{
//           marginBottom: "12px",
//           display: "flex",
//           justifyContent: "space-between",
//           alignItems: "center",
//         }}
//       >
//         <h2 style={{ margin: 0, fontSize: "18px" }}>Chart</h2>
//         <span style={{ color: "var(--text-muted)", fontSize: "14px" }}>
//           {selectedSymbol ?? "No symbol selected"}
//         </span>
//       </div>

//       <div
//         style={{
//           borderRadius: "6px",
//           border: "1px dashed var(--border)",
//           height: "260px",
//           display: "flex",
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
