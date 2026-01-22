export const model = {
  global: {},
  borders: [],
  layout: {
    type: "row",
    weight: 100,
    children: [
      {
        type: "tabset",
        weight: 50,
        children: [
          { type: "tab", name: "Scanner", component: "scanner" },
          { type: "tab", name: "News", component: "news" }
        ]
      },
      {
        type: "tabset",
        weight: 50,
        children: [
          { type: "tab", name: "Chart", component: "chart" },
          { type: "tab", name: "Level 2", component: "level2" },
          { type: "tab", name: "Tape", component: "tape" }
        ]
      }
    ]
  }
};
