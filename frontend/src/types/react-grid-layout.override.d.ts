declare module "react-grid-layout" {
  import * as React from "react";

  export interface LayoutItem {
    i: string;
    x: number;
    y: number;
    w: number;
    h: number;
    minW?: number;
    maxW?: number;
    minH?: number;
    maxH?: number;
    moved?: boolean;
    static?: boolean;
  }

  export interface ResponsiveProps {
    className?: string;
    layouts: Record<string, LayoutItem[]>;
    breakpoints: Record<string, number>;
    cols: Record<string, number>;
    margin?: [number, number];
    containerPadding?: [number, number];
    rowHeight: number;
    draggableCancel?: string;
    draggableHandle?: string;
    compactType?: string;
    children?: React.ReactNode;
  }

  export const Responsive: React.ComponentType<ResponsiveProps>;
}
