// Required for React 16 JSX transform
import React from "react";
import { DockviewReact } from "dockview"
import type { DockviewReadyEvent } from "dockview";


import LiveScannerPanel from "../components/LiveScannerPanel";
import Chart from "../components/ChartPanel";
import Level2 from "../components/Level2Panel";
import Tape from "../components/TapePanel";
import News from "../components/NewsPanel";


export default function DockviewWrapper() {
  const onReady = (event: DockviewReadyEvent) => {
    const { api } = event;

    api.addPanel({
      id: "scanner",
      component: "scanner",
      title: "Scanner",
      position: { direction: "left" }
    });

    api.addPanel({
      id: "chart",
      component: "chart",
      title: "Chart",
      position: { direction: "right" }
    });

    api.addPanel({
      id: "level2",
      component: "level2",
      title: "Level 2",
      position: { direction: "below" }
    });

    api.addPanel({
      id: "tape",
      component: "tape",
      title: "Tape",
      position: { direction: "right" }
    });

    api.addPanel({
      id: "news",
      component: "news",
      title: "News",
      position: { direction: "below" }
    });
  };

  return (
    <DockviewReact
      className="dockview-theme-dark"
      onReady={onReady}
      components={{
        scanner: LiveScannerPanel,
        chart: Chart,
        level2: Level2,
        tape: Tape,
        news: News
      }}
    />
  );
}
