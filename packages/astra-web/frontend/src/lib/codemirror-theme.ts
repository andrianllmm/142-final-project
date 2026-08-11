import { vscodeDarkInit } from "@uiw/codemirror-theme-vscode";

export const editorTheme = vscodeDarkInit({
  settings: {
    background: "var(--background)",
    gutterBackground: "var(--background)",
    lineHighlight: "var(--muted)",
  },
});
