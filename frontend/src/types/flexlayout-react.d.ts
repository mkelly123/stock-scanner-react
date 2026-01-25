declare module "flexlayout-react" {
  import * as React from "react";

  // Minimal JSON model shape FlexLayout expects
  export interface IJsonModel {
    global?: Record<string, unknown>;
    borders?: unknown[];
    layout: unknown;
  }

  // FlexLayout's internal model class
  export class Model {
    static fromJson(json: IJsonModel): Model;
    toJson(): IJsonModel;
  }

  // TabNode interface (only the parts your factory uses)
  export interface TabNode {
    getComponent(): string;
    getName(): string;
  }

  // Props for the Layout component
  export interface LayoutProps {
    model: Model;
    factory(node: TabNode): React.ReactNode;
  }

  // Layout is a class component in FlexLayout
  export class Layout extends React.Component<LayoutProps> {}
}
