import { useState } from "react";

export function usePanels() {
  const [visiblePanels, setVisiblePanels] = useState<string[]>([
    "scanner",
    "chart",
    "level2",
    "tape",
  ]);

  const [maximizedPanel, setMaximizedPanel] = useState<string | null>(null);

  const hidePanel = (panel: string) => {
    setVisiblePanels(prev => prev.filter(p => p !== panel));
  };

  const showPanel = (panel: string) => {
    setVisiblePanels(prev =>
      prev.includes(panel) ? prev : [...prev, panel]
    );
  };

  const toggleMaximize = (panel: string) => {
    setMaximizedPanel(prev => (prev === panel ? null : panel));
  };

  return {
    visiblePanels,
    maximizedPanel,
    hidePanel,
    showPanel,
    toggleMaximize,
  };
}
