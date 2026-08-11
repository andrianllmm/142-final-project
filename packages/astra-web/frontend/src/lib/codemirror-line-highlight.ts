import { RangeSetBuilder } from "@codemirror/state";
import { Decoration, DecorationSet, EditorView } from "@codemirror/view";

const highlightMark = Decoration.line({
  class: "cm-similarity-highlight",
});

export function highlightLines(lineNumbers: Iterable<number>) {
  const lineSet = new Set(lineNumbers);

  return EditorView.decorations.compute(["doc"], (state) => {
    const builder = new RangeSetBuilder<Decoration>();
    const totalLines = state.doc.lines;

    for (const lineNumber of [...lineSet].sort((a, b) => a - b)) {
      if (lineNumber < 1 || lineNumber > totalLines) {
        continue;
      }

      const line = state.doc.line(lineNumber);
      builder.add(line.from, line.from, highlightMark);
    }

    return builder.finish() as DecorationSet;
  });
}
