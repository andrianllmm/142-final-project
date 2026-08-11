import { useEffect, useMemo, useRef } from "react";
import { Columns2, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { cn } from "@/lib/utils";
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
    <article className="overflow-hidden rounded-lg border border-zinc-800 bg-zinc-950">
      <header className="flex min-h-[42px] items-center justify-between gap-2.5 border-b border-zinc-800 bg-zinc-900 px-3">
        <strong className="truncate text-sm text-zinc-100">{title}</strong>
        <span className="truncate text-xs text-zinc-400">
          {file.extension}
        </span>
      </header>
      <pre
        ref={preRef}
        className="m-0 grid max-h-[430px] overflow-auto py-2.5 font-mono text-[0.82rem] leading-[1.55] text-zinc-200"
      >
        {lines.map((line, index) => {
          const lineNumber = index + 1;
          const isHighlighted = highlightSet.has(lineNumber);

          return (
            <code
              className={cn(
                "grid grid-cols-[48px_minmax(0,1fr)] gap-3 bg-transparent px-3",
                isHighlighted &&
                  "bg-amber-400/20 shadow-[inset_3px_0_0_theme(colors.amber.400)]",
              )}
              data-line={lineNumber}
              key={`${file.id}-${lineNumber}`}
            >
              <span className="select-none text-right text-zinc-500">
                {lineNumber}
              </span>
              <span className="min-w-0 break-words whitespace-pre-wrap">
                {line || " "}
              </span>
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
