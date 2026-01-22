console.log("THIS IS THE REAL APP.TSX");

import FlexLayoutWrapper from "./layout/FlexLayoutWrapper";
import "./index.css";

export default function App() {
  return (
    <div style={{ width: "100vw", height: "100vh", overflow: "hidden" }}>
      <FlexLayoutWrapper />
    </div>
  );
}
