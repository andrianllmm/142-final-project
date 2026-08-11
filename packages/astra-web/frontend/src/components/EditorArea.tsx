import { useEffect, useMemo, useRef, useState } from "react";
import { Code2, Columns2, FileCode2, X } from "lucide-react";
import CodeMirror, { EditorView } from "@uiw/react-codemirror";
import { python } from "@codemirror/lang-python";
import { vscodeDark } from "@uiw/codemirror-theme-vscode";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { highlightLines } from "@/lib/codemirror-line-highlight";
import { cn } from "@/lib/utils";
import { SimilarityResult, SimilarityStatus, UploadedCodeFile } from "@/types";

interface EditorAreaProps {
  files: UploadedCodeFile[];
  activeFileId: string;
  selectedResult: SimilarityResult | null;
  onSelectFile: (fileId: string) => void;
  onContentChange: (fileId: string, content: string) => void;
  onCloseDiff: () => void;
}

export function EditorArea({
  files,
  activeFileId,
  selectedResult,
  onSelectFile,
  onContentChange,
  onCloseDiff,
}: EditorAreaProps) {
  if (selectedResult) {
    return <DiffView result={selectedResult} onClose={onCloseDiff} />;
  }

  const activeFile = files.find((file) => file.id === activeFileId) ?? null;

  if (files.length === 0 || !activeFile) {
    return (
      <div className="grid h-full place-items-center gap-2 text-center">
        <Code2 className="mx-auto text-muted-foreground" size={32} />
        <h2 className="font-semibold">No file open</h2>
        <p className="text-sm text-muted-foreground">
          Upload or select a Python file from the explorer to start editing.
        </p>
      </div>
    );
  }

  return (
    <div className="flex h-full flex-col">
      <Tabs value={activeFile.id} onValueChange={onSelectFile}>
        <TabsList className="h-10 w-full justify-start rounded-none border-b bg-transparent px-2">
          {files.map((file) => (
            <TabsTrigger key={file.id} value={file.id} className="gap-1.5">
              <FileCode2 size={14} />
              {file.name}
            </TabsTrigger>
          ))}
        </TabsList>
      </Tabs>
      <div className="min-h-0 flex-1">
        <CodeMirror
          key={activeFile.id}
          value={activeFile.content}
          theme={vscodeDark}
          extensions={[python(), EditorView.lineWrapping]}
          basicSetup={{ foldGutter: false }}
          height="100%"
          className="h-full text-sm [&_.cm-editor]:h-full"
          onChange={(value) => onContentChange(activeFile.id, value)}
        />
      </div>
    </div>
  );
}

function DiffView({
  result,
  onClose,
}: {
  result: SimilarityResult;
  onClose: () => void;
}) {
  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between gap-3 border-b px-4 py-2.5">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-base font-semibold">
              {Math.round(result.score * 100)}% match
            </h2>
            <StatusBadge status={result.status} />
          </div>
          <div className="mt-0.5 flex flex-wrap items-center gap-1.5 text-xs text-muted-foreground">
            <span>{result.fileA.name}</span>
            <Columns2 size={12} />
            <span>{result.fileB.name}</span>
          </div>
        </div>
        <Button
          variant="outline"
          size="icon-sm"
          aria-label="Close diff view"
          onClick={onClose}
        >
          <X size={16} />
        </Button>
      </div>
      <div className="grid min-h-0 flex-1 grid-cols-2 divide-x">
        <DiffPane file={result.fileA} highlightedLines={result.highlights.left} />
        <DiffPane file={result.fileB} highlightedLines={result.highlights.right} />
      </div>
    </div>
  );
}

const statusBadgeVariant: Record<
  SimilarityStatus,
  "secondary" | "outline" | "destructive"
> = {
  low: "secondary",
  medium: "outline",
  high: "destructive",
};

function StatusBadge({ status }: { status: SimilarityStatus }) {
  const label =
    status === "high"
      ? "High similarity"
      : status === "medium"
        ? "Medium similarity"
        : "Low similarity";

  return <Badge variant={statusBadgeVariant[status]}>{label}</Badge>;
}

function DiffPane({
  file,
  highlightedLines,
}: {
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

  const fileIdRef = useRef(file.id);
  fileIdRef.current = file.id;

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
      effects: EditorView.scrollIntoView(line.from, { y: "center" }),
    });
  }, [sortedHighlights, view]);

  return (
    <div className="flex min-w-0 flex-col">
      <header className="flex min-h-9 items-center justify-between gap-2.5 border-b px-3">
        <strong className="truncate text-xs font-medium">{file.name}</strong>
        <span className="truncate text-xs text-muted-foreground">
          {file.extension}
        </span>
      </header>
      <div className={cn("min-h-0 flex-1")}>
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
          height="100%"
          className="h-full text-[0.82rem] [&_.cm-editor]:h-full"
          onCreateEditor={(editorView) => setView(editorView)}
        />
      </div>
    </div>
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
