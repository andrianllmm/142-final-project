import { useEffect, useState } from "react";
import { PanelLeft, PanelRight } from "lucide-react";
import { AppSidebar } from "@/components/app-sidebar";
import { AnalysisSidebar } from "@/components/analysis-sidebar";
import { EditorArea } from "@/components/EditorArea";
import { Button } from "@/components/ui/button";
import { SidebarProvider } from "@/components/ui/sidebar";

import { getExtension, isSupportedFile } from "./services/analysisUtils";
import { analyzeCodeSimilarity } from "./services/analyzeApi";
import { SimilarityResult, UploadedCodeFile } from "./types";

const FILE_STORAGE_KEY = "astra.uploadedFiles";

function App() {
  const [files, setFiles] = useState<UploadedCodeFile[]>(loadStoredFiles);
  const [openFileIds, setOpenFileIds] = useState<string[]>([]);
  const [activeFileId, setActiveFileId] = useState("");
  const [threshold, setThreshold] = useState(0.8);
  const [results, setResults] = useState<SimilarityResult[]>([]);
  const [selectedResult, setSelectedResult] = useState<SimilarityResult | null>(
    null,
  );
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isReadingFiles, setIsReadingFiles] = useState(false);
  const [notice, setNotice] = useState("Only Python .py files are supported.");
  const [isExplorerOpen, setIsExplorerOpen] = useState(true);
  const [isAnalysisOpen, setIsAnalysisOpen] = useState(true);

  useEffect(() => {
    try {
      localStorage.setItem(FILE_STORAGE_KEY, JSON.stringify(files));
    } catch (error) {
      console.error("Unable to save uploaded files locally.", error);
      setNotice("Files are loaded, but could not be saved in local storage.");
    }
  }, [files]);

  useEffect(() => {
    if (files.length > 0) {
      const firstId = files[0].id;
      setActiveFileId(firstId);
      setOpenFileIds((ids) => (ids.includes(firstId) ? ids : [...ids, firstId]));
    }
    // Only auto-open a file once, when the app first loads with stored files.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handleFilesAdded(incomingFiles: File[]) {
    const supportedFiles = incomingFiles.filter((file) =>
      isSupportedFile(file.name),
    );
    const rejectedCount = incomingFiles.length - supportedFiles.length;

    if (supportedFiles.length === 0) {
      setNotice(
        rejectedCount > 0
          ? "Only Python .py files are supported."
          : "Select files to continue.",
      );
      return;
    }

    setIsReadingFiles(true);

    try {
      const preparedFiles = await Promise.all(
        supportedFiles.map(async (file) => ({
          id: createFileId(file),
          name: file.name,
          extension: getExtension(file.name),
          type: getReadableFileType(file),
          size: file.size,
          content: await file.text(),
          lastModified: file.lastModified,
        })),
      );

      setFiles((currentFiles) => [...currentFiles, ...preparedFiles]);
      setOpenFileIds((ids) => [...ids, ...preparedFiles.map((file) => file.id)]);
      setActiveFileId(preparedFiles[0].id);
      setResults([]);
      setSelectedResult(null);
      setNotice(
        rejectedCount > 0
          ? `${preparedFiles.length} files added. ${rejectedCount} unsupported files skipped.`
          : `${preparedFiles.length} files added.`,
      );
    } finally {
      setIsReadingFiles(false);
    }
  }

  function handleRemoveFile(fileId: string) {
    const tabIndex = openFileIds.indexOf(fileId);
    const nextOpenIds = openFileIds.filter((id) => id !== fileId);

    setFiles((currentFiles) => currentFiles.filter((file) => file.id !== fileId));
    setOpenFileIds(nextOpenIds);

    if (activeFileId === fileId) {
      setActiveFileId(nextOpenIds[tabIndex] ?? nextOpenIds[tabIndex - 1] ?? "");
    }

    setResults([]);
    setSelectedResult(null);
    setNotice("File removed. Run a new check to refresh the report.");
  }

  function handleCloseTab(fileId: string) {
    const tabIndex = openFileIds.indexOf(fileId);
    if (tabIndex === -1) {
      return;
    }

    const nextOpenIds = openFileIds.filter((id) => id !== fileId);
    setOpenFileIds(nextOpenIds);

    if (activeFileId === fileId) {
      setActiveFileId(nextOpenIds[tabIndex] ?? nextOpenIds[tabIndex - 1] ?? "");
    }
  }

  function handleContentChange(fileId: string, content: string) {
    setFiles((currentFiles) =>
      currentFiles.map((file) =>
        file.id === fileId
          ? {
              ...file,
              content,
              size: getUtf8ByteSize(content),
              lastModified: Date.now(),
            }
          : file,
      ),
    );
  }

  async function handleStartAnalysis() {
    if (files.length < 2) {
      return;
    }

    setIsAnalyzing(true);
    setSelectedResult(null);

    try {
      const analysis = await analyzeCodeSimilarity({
        files,
        threshold,
      });

      setResults(analysis.results);
      setNotice(analysis.message);
    } finally {
      setIsAnalyzing(false);
    }
  }

  function handleSelectFile(fileId: string) {
    setSelectedResult(null);
    setOpenFileIds((ids) => (ids.includes(fileId) ? ids : [...ids, fileId]));
    setActiveFileId(fileId);
  }

  const openFiles = openFileIds
    .map((id) => files.find((file) => file.id === id))
    .filter((file): file is UploadedCodeFile => Boolean(file));

  return (
    <div className="flex h-screen w-screen overflow-hidden">
      <SidebarProvider
        open={isExplorerOpen}
        onOpenChange={setIsExplorerOpen}
        className="w-auto"
        style={{ "--sidebar-width": "17rem" } as React.CSSProperties}
      >
        <AppSidebar
          files={files}
          activeFileId={activeFileId}
          isReading={isReadingFiles}
          onFilesAdded={handleFilesAdded}
          onSelectFile={handleSelectFile}
          onRemoveFile={handleRemoveFile}
        />
      </SidebarProvider>

      <div className="flex min-w-0 flex-1 flex-col bg-background">
        <header className="flex h-10 shrink-0 items-center justify-between border-b px-2">
          <Button
            variant="ghost"
            size="icon-sm"
            aria-label="Toggle file explorer"
            onClick={() => setIsExplorerOpen((open) => !open)}
          >
            <PanelLeft />
          </Button>
          <Button
            variant="ghost"
            size="icon-sm"
            aria-label="Toggle analysis panel"
            onClick={() => setIsAnalysisOpen((open) => !open)}
          >
            <PanelRight />
          </Button>
        </header>
        <div className="min-h-0 flex-1">
          <EditorArea
            openFiles={openFiles}
            activeFileId={activeFileId}
            selectedResult={selectedResult}
            onSelectFile={handleSelectFile}
            onCloseTab={handleCloseTab}
            onContentChange={handleContentChange}
            onCloseDiff={() => setSelectedResult(null)}
          />
        </div>
      </div>

      <SidebarProvider
        open={isAnalysisOpen}
        onOpenChange={setIsAnalysisOpen}
        className="w-auto"
        style={{ "--sidebar-width": "20rem" } as React.CSSProperties}
      >
        <AnalysisSidebar
          fileCount={files.length}
          threshold={threshold}
          isAnalyzing={isAnalyzing}
          comparisons={results}
          selectedResultId={selectedResult?.id ?? null}
          onThresholdChange={setThreshold}
          onStart={handleStartAnalysis}
          onViewDetails={setSelectedResult}
        />
      </SidebarProvider>
    </div>
  );
}

function loadStoredFiles(): UploadedCodeFile[] {
  try {
    const storedFiles = localStorage.getItem(FILE_STORAGE_KEY);
    if (!storedFiles) {
      return [];
    }

    const parsedFiles: unknown = JSON.parse(storedFiles);
    return Array.isArray(parsedFiles)
      ? parsedFiles.filter(isUploadedCodeFile)
      : [];
  } catch (error) {
    console.error("Unable to load uploaded files from local storage.", error);
    return [];
  }
}

function isUploadedCodeFile(file: unknown): file is UploadedCodeFile {
  if (!file || typeof file !== "object") {
    return false;
  }

  const candidate = file as Partial<UploadedCodeFile>;
  return (
    typeof candidate.id === "string" &&
    typeof candidate.name === "string" &&
    typeof candidate.extension === "string" &&
    typeof candidate.type === "string" &&
    typeof candidate.size === "number" &&
    typeof candidate.content === "string" &&
    typeof candidate.lastModified === "number"
  );
}

function createFileId(file: File): string {
  const randomValue =
    typeof crypto !== "undefined" && "randomUUID" in crypto
      ? crypto.randomUUID()
      : Math.random().toString(36).slice(2);

  return `${file.name}-${file.lastModified}-${randomValue}`;
}

function getReadableFileType(file: File): string {
  return getExtension(file.name) === ".py" ? "Python source" : "Code source";
}

function getUtf8ByteSize(content: string): number {
  return new TextEncoder().encode(content).length;
}

export default App;
