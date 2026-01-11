type Props = {
  data: any[];
};

export default function ResultsTable({ data }: Props) {
  return <div>Results Table Loaded ({data.length} rows)</div>;
}
