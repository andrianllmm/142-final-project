import { useEffect, useMemo, useRef, useState } from "react";
import { Columns2, X } from "lucide-react";
import CodeMirror, { EditorView } from "@uiw/react-codemirror";
import { python } from "@codemirror/lang-python";
import { vscodeDark } from "@uiw/codemirror-theme-vscode";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { highlightLines } from "@/lib/codemirror-line-highlight";
import { SimilarityResult, UploadedCodeFile } from "../types";
import { StatusBadge } from "./ResultsTable";

interface SimilarityDetailViewProps {
  result: SimilarityResult;
  onClose: () => void;
}

export function SimilarityDetailView({
  result,
  onClose,
}: SimilarityDetailViewProps) {
  const detailRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    detailRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, [result.id]);

  return (
    <div ref={detailRef}>
      <Card aria-label="Similarity details" className="shadow-lg">
        <CardHeader className="flex-row items-start justify-between gap-3">
          <div>
            <h2 className="mt-1 mb-2 text-2xl font-semibold">
              {Math.round(result.score * 100)}% match
            </h2>
            <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
              <span>{result.fileA.name}</span>
              <Columns2 size={15} />
              <span>{result.fileB.name}</span>
              <StatusBadge status={result.status} />
            </div>
          </div>
          <Button
            variant="outline"
            size="icon-sm"
            aria-label="Close detail view"
            onClick={onClose}
          >
            <X size={18} />
          </Button>
        </CardHeader>
        <CardContent>
          <div className="grid gap-3.5 sm:grid-cols-2">
            <CodePane
              title={result.fileA.name}
              file={result.fileA}
              highlightedLines={result.highlights.left}
            />
            <CodePane
              title={result.fileB.name}
              file={result.fileB}
              highlightedLines={result.highlights.right}
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function CodePane({
  title,
  file,
  highlightedLines,
}: {
  title: string;
  file: UploadedCodeFile;
  highlightedLines: number[];
}) {
  const content = ensureDisplayContent(file);
  const [view, setView] = useState<EditorView | null>(null);
  const sortedHighlights = useMemo(
    () => [...new Set(highlightedLines)].sort((left, right) => left - right),
    [highlightedLines],
  );

  const extensions = useMemo(
    () => [
      python(),
      EditorView.lineWrapping,
      EditorView.editable.of(false),
      highlightLines(sortedHighlights),
    ],
    [sortedHighlights],
  );

  useEffect(() => {
    if (!view) {
      return;
    }

    const firstHighlightedLine = sortedHighlights[0];
    if (!firstHighlightedLine) {
      view.scrollDOM.scrollTo({ top: 0 });
      return;
    }

    const totalLines = view.state.doc.lines;
    if (firstHighlightedLine > totalLines) {
      return;
    }

    const line = view.state.doc.line(firstHighlightedLine);
    view.dispatch({
      effects: EditorView.scrollIntoView(line.from, {
        y: "center",
      }),
    });
  }, [file.id, sortedHighlights, view]);

  return (
    <article className="overflow-hidden rounded-lg border border-zinc-800 bg-zinc-950">
      <header className="flex min-h-[42px] items-center justify-between gap-2.5 border-b border-zinc-800 bg-zinc-900 px-3">
        <strong className="truncate text-sm text-zinc-100">{title}</strong>
        <span className="truncate text-xs text-zinc-400">
          {file.extension}
        </span>
      </header>
      <CodeMirror
        value={content}
        theme={vscodeDark}
        extensions={extensions}
        editable={false}
        basicSetup={{
          lineNumbers: true,
          foldGutter: false,
          highlightActiveLine: false,
          highlightActiveLineGutter: false,
        }}
        height="430px"
        className="text-[0.82rem]"
        onCreateEditor={(editorView) => setView(editorView)}
      />
    </article>
  );
}

function ensureDisplayContent(file: UploadedCodeFile): string {
  if (file.content.trim()) {
    return file.content;
  }

  return [
    `# ${file.name}`,
    "def normalize_submission(source):",
    "    tokens = tokenize(source)",
    "    cleaned = [token for token in tokens if token]",
    "    return [token.lower() for token in cleaned]",
    "",
    "",
    "def compare_submission(source, target):",
    "    return normalize_submission(source) == normalize_submission(target)",
  ].join("\n");
}
