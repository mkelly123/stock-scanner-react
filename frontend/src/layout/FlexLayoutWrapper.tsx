// Required for React 16 JSX transform
import React from "react";
import { Layout } from "flexlayout-react";
import type { TabNode } from "flexlayout-react";

import { model } from "./layoutModel";

import LiveScannerPanel from "../components/LiveScannerPanel";
import Chart from "../components/ChartPanel";
import Level2 from "../components/Level2Panel";
import Tape from "../components/TapePanel";
import News from "../components/NewsPanel";

import "flexlayout-react/style/light.css";

export default function FlexLayoutWrapper() {
  const factory = (node: TabNode) => {
    const component = node.getComponent();

    switch (component) {
      case "scanner":
        return <LiveScannerPanel />;   // ← LIVE MODE HERE
      case "chart":
        return <Chart />;
      case "level2":
        return <Level2 />;
      case "tape":
        return <Tape />;
      case "news":
        return <News />;
      default:
        return <div>Unknown component</div>;
    }
  };

  return (
    <div style={{ height: "100vh", width: "100vw" }}>
      <Layout model={model} factory={factory} />
    </div>
  );
}
