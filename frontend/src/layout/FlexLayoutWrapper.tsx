import { Layout, TabNode, Model } from "flexlayout-react";
import "flexlayout-react/style/light.css";
import { model } from "./layoutModel";

import Scanner from "../components/ScannerPanel";
import Chart from "../components/ChartPanel";
import Level2 from "../components/Level2Panel";
import Tape from "../components/TapePanel";
import News from "../components/NewsPanel";

export default function FlexLayoutWrapper() {
  const factory = (node: TabNode) => {
    const component = node.getComponent();

    switch (component) {
      case "scanner":
        return <Scanner />;
      case "chart":
        return <Chart />;
      case "level2":
        return <Level2 />;
      case "tape":
        return <Tape />;
      case "news":
        return <News />;
      default:
        return <div>Unknown component: {component}</div>;
    }
  };

  return <Layout model={Model.fromJson(model)} factory={factory} />;
}
