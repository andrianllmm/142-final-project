import { useEffect, useState } from "react";
import { AnalysisSettings } from "./components/AnalysisSettings";
import { FileUpload } from "./components/FileUpload";
import { ResultsSummary } from "./components/ResultsSummary";
import { ResultsTable } from "./components/ResultsTable";
import { SimilarityDetailView } from "./components/SimilarityDetailView";

import { getExtension, isSupportedFile } from "./services/analysisUtils";
import { analyzeCodeSimilarity } from "./services/analyzeApi";
import { SimilarityResult, UploadedCodeFile } from "./types";

const FILE_STORAGE_KEY = "astra.uploadedFiles";

function App() {
  const [files, setFiles] = useState<UploadedCodeFile[]>(loadStoredFiles);
  const [threshold, setThreshold] = useState(0.8);
  const [results, setResults] = useState<SimilarityResult[]>([]);
  const [selectedResult, setSelectedResult] = useState<SimilarityResult | null>(
    null,
  );
  const [editingFileId, setEditingFileId] = useState("");
  const [editingContent, setEditingContent] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isReadingFiles, setIsReadingFiles] = useState(false);
  const [isSavingEdit, setIsSavingEdit] = useState(false);
  const [notice, setNotice] = useState("Only Python .py files are supported.");

  useEffect(() => {
    try {
      localStorage.setItem(FILE_STORAGE_KEY, JSON.stringify(files));
    } catch (error) {
      console.error("Unable to save uploaded files locally.", error);
      setNotice("Files are loaded, but could not be saved in local storage.");
    }
  }, [files]);

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
    setFiles((currentFiles) =>
      currentFiles.filter((file) => file.id !== fileId),
    );
    setResults([]);
    setSelectedResult(null);
    if (editingFileId === fileId) {
      setEditingFileId("");
      setEditingContent("");
    }
    setNotice("File removed. Run a new check to refresh the report.");
  }

  function handleOpenFileEditor(fileId: string) {
    const fileToEdit = files.find((file) => file.id === fileId);
    if (!fileToEdit) {
      return;
    }

    setEditingFileId(fileId);
    setEditingContent(fileToEdit.content);
  }

  function handleCancelFileEdit() {
    setEditingFileId("");
    setEditingContent("");
  }

  async function handleSaveFileEdit() {
    if (!editingFileId || isAnalyzing || isSavingEdit) {
      return;
    }

    const currentFile = files.find((file) => file.id === editingFileId);
    if (!currentFile) {
      handleCancelFileEdit();
      return;
    }

    const shouldRerunAnalysis = results.length > 0 && files.length >= 2;
    const updatedFiles = files.map((file) =>
      file.id === editingFileId
        ? {
            ...file,
            content: editingContent,
            size: getUtf8ByteSize(editingContent),
            lastModified: Date.now(),
          }
        : file,
    );

    setIsSavingEdit(true);
    setFiles(updatedFiles);
    setSelectedResult(null);
    setEditingFileId("");
    setEditingContent("");

    if (!shouldRerunAnalysis) {
      setNotice(`${currentFile.name} saved.`);
      setIsSavingEdit(false);
      return;
    }

    setIsAnalyzing(true);

    try {
      const analysis = await analyzeCodeSimilarity({
        files: updatedFiles,
        threshold,
      });

      setResults(analysis.results);
      setNotice(`${currentFile.name} saved. ${analysis.message}`);
      window.setTimeout(() => scrollToReports(), 0);
    } finally {
      setIsAnalyzing(false);
      setIsSavingEdit(false);
    }
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
      window.setTimeout(() => scrollToReports(), 0);
    } finally {
      setIsAnalyzing(false);
    }
  }

  return (
    <div className="app-shell">
      <main className="app-main">
        <div className="workspace-grid">
          <div className="workspace-left">
            <FileUpload
              files={files}
              isReading={isReadingFiles}
              notice={notice}
              onFilesAdded={handleFilesAdded}
              onRemoveFile={handleRemoveFile}
              onEditFile={handleOpenFileEditor}
            />
          </div>

          <div className="workspace-right">
            <AnalysisSettings
              files={files}
              threshold={threshold}
              isAnalyzing={isAnalyzing}
              onThresholdChange={setThreshold}
              onStart={handleStartAnalysis}
            />

            <ResultsSummary
              totalFiles={files.length}
              threshold={threshold}
              results={results}
            />

            {selectedResult ? (
              <SimilarityDetailView
                result={selectedResult}
                onClose={() => setSelectedResult(null)}
              />
            ) : null}

            <div id="reports-section">
              <ResultsTable
                results={results}
                threshold={threshold}
                onViewDetails={setSelectedResult}
              />
            </div>
          </div>
        </div>
      </main>

      {editingFileId ? (
        <FileEditModal
          fileName={
            files.find((file) => file.id === editingFileId)?.name ??
            "Uploaded file"
          }
          content={editingContent}
          isSaving={isSavingEdit || isAnalyzing}
          onContentChange={setEditingContent}
          onCancel={handleCancelFileEdit}
          onSave={handleSaveFileEdit}
        />
      ) : null}
    </div>
  );
}

interface FileEditModalProps {
  fileName: string;
  content: string;
  isSaving: boolean;
  onContentChange: (content: string) => void;
  onCancel: () => void;
  onSave: () => void;
}

function FileEditModal({
  fileName,
  content,
  isSaving,
  onContentChange,
  onCancel,
  onSave,
}: FileEditModalProps) {
  return (
    <div className="modal-backdrop" role="presentation">
      <section
        className="code-edit-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="code-edit-title"
      >
        <div className="modal-header">
          <div>
            <p className="eyebrow">Edit uploaded code</p>
            <h2 id="code-edit-title">{fileName}</h2>
          </div>
        </div>

        <label className="code-editor-label" htmlFor="uploaded-code-editor">
          Code content
          <textarea
            id="uploaded-code-editor"
            className="code-editor-textarea"
            value={content}
            spellCheck={false}
            onChange={(event) => onContentChange(event.target.value)}
          />
        </label>

        <div className="modal-actions">
          <button
            className="secondary-action"
            type="button"
            disabled={isSaving}
            onClick={onCancel}
          >
            Cancel
          </button>
          <button
            className="primary-action modal-save-action"
            type="button"
            disabled={isSaving}
            onClick={onSave}
          >
            {isSaving ? "Updating report..." : "Save"}
          </button>
        </div>
      </section>
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

function scrollToReports() {
  document
    .getElementById("reports-section")
    ?.scrollIntoView({ behavior: "smooth", block: "start" });
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
