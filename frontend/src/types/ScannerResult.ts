export type ScannerResult = {
  symbol: string;
  score: number;
  volume: number;
  price: number;
  trend: string;
  history?: number[];
};
