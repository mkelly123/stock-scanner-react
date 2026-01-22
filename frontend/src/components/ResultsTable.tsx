import type { ResultRow } from "../types";

interface Props {
  results: ResultRow[];
  onSelectSymbol: (symbol: string) => void;
  selectedSymbol: string | null;
}

export default function ResultsTable({
  results,
  onSelectSymbol,
  selectedSymbol
}: Props) {
  return (
    <table className="results-table">
      <thead>
        <tr>
          <th>Symbol</th>
          <th>Price</th>
          <th>Vol</th>
          <th>Float</th>
          <th>RelVol</th>
          <th>%Chg</th>
        </tr>
      </thead>

      <tbody>
        {results.map((row) => (
          <tr
            key={row.symbol}
            className={row.symbol === selectedSymbol ? "selected" : ""}
            onClick={() => onSelectSymbol(row.symbol)}
          >
            <td>{row.symbol}</td>
            <td>{row.price.toFixed(2)}</td>
            <td>{row.volume.toLocaleString()}</td>
            <td>{row.float.toLocaleString()}</td>
            <td>{row.relVolume.toFixed(2)}</td>
            <td className={row.changePct >= 0 ? "green" : "red"}>
              {row.changePct.toFixed(2)}%
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
