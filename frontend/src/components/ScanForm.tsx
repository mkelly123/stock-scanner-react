type Props = {
  onScan: () => void;
};

export default function ScanForm({ onScan }: Props) {
  return (
    <div>
      <button onClick={onScan}>Run Scan</button>
    </div>
  );
}
