import { useEffect, useMemo, useRef } from "react";
import { CheckCircle2, Columns2, X } from "lucide-react";
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
  const detailRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    detailRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, [result.id]);

  return (
    <section
      ref={detailRef}
      className="panel detail-panel"
      aria-label="Similarity details"
    >
      <div className="detail-header">
        <div>
          <h2>{Math.round(result.score * 100)}% match</h2>
          <div className="detail-meta">
            <span>{result.fileA.name}</span>
            <Columns2 size={15} />
            <span>{result.fileB.name}</span>
            <StatusBadge status={result.status} />
          </div>
        </div>
        <button
          className="icon-button"
          type="button"
          aria-label="Close detail view"
          onClick={onClose}
        >
          <X size={18} />
        </button>
      </div>

      <div className="code-split">
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
    </section>
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
  const lines = ensureDisplayLines(file);
  const preRef = useRef<HTMLPreElement | null>(null);
  const sortedHighlights = useMemo(
    () => [...new Set(highlightedLines)].sort((left, right) => left - right),
    [highlightedLines],
  );
  const highlightSet = new Set(sortedHighlights);

  useEffect(() => {
    const firstHighlightedLine = sortedHighlights[0];
    if (!firstHighlightedLine || !preRef.current) {
      preRef.current?.scrollTo({ top: 0 });
      return;
    }

    const target = preRef.current.querySelector<HTMLElement>(
      `[data-line="${firstHighlightedLine}"]`,
    );

    if (!target) {
      return;
    }

    preRef.current.scrollTo({
      top: Math.max(target.offsetTop - preRef.current.clientHeight * 0.28, 0),
      behavior: "smooth",
    });
  }, [file.id, sortedHighlights]);

  return (
    <article className="code-pane">
      <header>
        <strong>{title}</strong>
        <span>{file.extension}</span>
      </header>
      <pre ref={preRef}>
        {lines.map((line, index) => {
          const lineNumber = index + 1;
          const isHighlighted = highlightSet.has(lineNumber);

          return (
            <code
              className={isHighlighted ? "is-highlighted" : ""}
              data-line={lineNumber}
              key={`${file.id}-${lineNumber}`}
            >
              <span className="line-number">{lineNumber}</span>
              <span className="line-code">{line || " "}</span>
            </code>
          );
        })}
      </pre>
    </article>
  );
}

function ensureDisplayLines(file: UploadedCodeFile): string[] {
  const realLines = file.content.split(/\r?\n/);
  if (realLines.length > 1 || realLines[0]?.trim()) {
    return realLines;
  }

  return [
    `// ${file.name}`,
    "function normalizeSubmission(input) {",
    "  const tokens = tokenize(input);",
    "  const cleaned = tokens.filter(Boolean);",
    "  return cleaned.map((token) => token.toLowerCase());",
    "}",
    "",
    "export function compareSubmission(source, target) {",
    "  return normalizeSubmission(source).join('|') ===",
    "    normalizeSubmission(target).join('|');",
    "}",
  ];
}
