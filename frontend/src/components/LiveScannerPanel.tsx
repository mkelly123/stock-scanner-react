import React, { useEffect, useState } from "react";
import Tabs from "./Tabs";
import ScannerTable from "./ScannerTable";


export interface ScannerResult {
  symbol: string;
  price: number;
  changePct: number;
  volume: number;
  relVolume: number;
  trend?: string;
  intradayScore?: number;
  swingScore?: number;
  combinedScore?: number;
  strategy: string;
  [key: string]: unknown; // allows extra fields without errors
}

export default function LiveScannerPanel() {
  const [intradayData, setIntradayData] = useState<ScannerResult[]>([]);
  const [swingData, setSwingData] = useState<ScannerResult[]>([]);

  // Fetch intraday data
  useEffect(() => {
    fetch("http://localhost:8000/api/scan/momentum?strategy=intraday")
      .then((res) => res.json())
      .then((data) => setIntradayData(data))
      .catch((err) => console.error("Intraday fetch error:", err));
  }, []);

  // Fetch swing data
  useEffect(() => {
    fetch("http://localhost:8000/api/scan/momentum?strategy=swing")
      .then((res) => res.json())
      .then((data) => setSwingData(data))
      .catch((err) => console.error("Swing fetch error:", err));
  }, []);

  useEffect(() => {
    console.log("Updated Swing data:", swingData);
  }, [swingData]);



  return (
    <Tabs
      tabs={[
        {
          label: "Intraday",
          content: () => (
            <div>
              <h3>Intraday Scanner</h3>
              <ScannerTable data={intradayData} />
            </div>
          ),
        },
        {
          label: "Swing",
          content: () => (
            <div>
              <h3>Swing Scanner</h3>
              <ScannerTable data={swingData} />
            </div>
          ),
        },
      ]}
    />

  );
}
