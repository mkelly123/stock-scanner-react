export interface ResultRow {
  symbol: string;
  price: number;
  volume: number;
  float: number;
  relVolume: number;
  changePct: number;
  score?: number;   // optional
  trend?: string;   // optional
}

