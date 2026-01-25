import { Model } from "flexlayout-react";

export const layoutJson = {
  global: {},
  borders: [],
  layout: {
    type: "row",
    weight: 100,
    children: [
      {
        type: "row",
        weight: 40,
        children: [
          {
            type: "tabset",
            weight: 50,
            children: [
              {
                type: "tab",
                name: "Scanner",
                component: "scanner"
              }
            ]
          },
          {
            type: "tabset",
            weight: 50,
            children: [
              {
                type: "tab",
                name: "Chart",
                component: "chart"
              }
            ]
          }
        ]
      },
      {
        type: "row",
        weight: 30,
        children: [
          {
            type: "tabset",
            weight: 50,
            children: [
              {
                type: "tab",
                name: "Level 2",
                component: "level2"
              }
            ]
          },
          {
            type: "tabset",
            weight: 50,
            children: [
              {
                type: "tab",
                name: "Tape",
                component: "tape"
              }
            ]
          }
        ]
      },
      {
        type: "tabset",
        weight: 30,
        children: [
          {
            type: "tab",
            name: "News",
            component: "news"
          }
        ]
      }
    ]
  }
};

export const model = Model.fromJson(layoutJson);
