import { useEffect, useMemo, useState } from "react";
import { AlertCircle, CheckCircle2, GraduationCap } from "lucide-react";
import { AnalysisSettings } from "./components/AnalysisSettings";
import { FileUpload } from "./components/FileUpload";
import { ResultsSummary } from "./components/ResultsSummary";
import { ResultsTable } from "./components/ResultsTable";
import { Sidebar } from "./components/Sidebar";
import { SimilarityDetailView } from "./components/SimilarityDetailView";
import { ProjectInfo } from "./components/ProjectInfo";
import {
  getExtension,
  isSupportedFile
} from "./services/mockAnalysis";
import { analyzeCodeSimilarity } from "./services/analyzeApi";
import {
  AnalysisPayload,
  ComparisonMode,
  SimilarityResult,
  UploadedCodeFile
} from "./types";

type SidebarItem =
  | "dashboard"
  | "new-analysis"
  | "reports"
  | "settings"
  | "project-info";

const sectionIds: Record<SidebarItem, string> = {
  dashboard: "dashboard-section",
  "new-analysis": "new-analysis-section",
  reports: "reports-section",
  settings: "settings-section",
  "project-info": "project-info-section"
};

function App() {
  const [activeItem, setActiveItem] = useState<SidebarItem>("dashboard");
  const [files, setFiles] = useState<UploadedCodeFile[]>([]);
  const [threshold, setThreshold] = useState(0.8);
  const [comparisonMode, setComparisonMode] =
    useState<ComparisonMode>("all_pairs");
  const [referenceFileId, setReferenceFileId] = useState("");
  const [results, setResults] = useState<SimilarityResult[]>([]);
  const [selectedResult, setSelectedResult] = useState<SimilarityResult | null>(
    null
  );
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isReadingFiles, setIsReadingFiles] = useState(false);
  const [notice, setNotice] = useState("Only Python .py files are supported.");
  const [lastPayload, setLastPayload] = useState<AnalysisPayload | null>(null);

  useEffect(() => {
    if (files.length === 0) {
      setReferenceFileId("");
      return;
    }

    const referenceStillExists = files.some((file) => file.id === referenceFileId);
    if (!referenceStillExists) {
      setReferenceFileId(files[0].id);
    }
  }, [files, referenceFileId]);

  const flaggedCount = useMemo(
    () => results.filter((result) => result.score >= threshold).length,
    [results, threshold]
  );

  async function handleFilesAdded(incomingFiles: File[]) {
    const supportedFiles = incomingFiles.filter((file) =>
      isSupportedFile(file.name)
    );
    const rejectedCount = incomingFiles.length - supportedFiles.length;

    if (supportedFiles.length === 0) {
      setNotice(
        rejectedCount > 0
          ? "Only Python .py files are supported."
          : "Select files to continue."
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
          lastModified: file.lastModified
        }))
      );

      setFiles((currentFiles) => [...currentFiles, ...preparedFiles]);
      setResults([]);
      setSelectedResult(null);
      setNotice(
        rejectedCount > 0
          ? `${preparedFiles.length} files added. ${rejectedCount} unsupported files skipped.`
          : `${preparedFiles.length} files added.`
      );
    } finally {
      setIsReadingFiles(false);
    }
  }

  function handleRemoveFile(fileId: string) {
    setFiles((currentFiles) => currentFiles.filter((file) => file.id !== fileId));
    setResults([]);
    setSelectedResult(null);
    setNotice("File removed. Run a new check to refresh the report.");
  }

  async function handleStartAnalysis() {
    if (files.length < 2) {
      return;
    }

    setIsAnalyzing(true);
    setSelectedResult(null);

    const analysis = await analyzeCodeSimilarity({
      files,
      threshold,
      comparisonMode,
      referenceFileId
    });

    setLastPayload(analysis.payload);
    setResults(analysis.results);
    setNotice(analysis.message);
    setIsAnalyzing(false);
    setActiveItem("reports");
    window.setTimeout(() => scrollToSection("reports"), 0);
  }

  function handleSidebarSelect(item: SidebarItem) {
    setActiveItem(item);
    scrollToSection(item);
  }

  return (
    <div className="app-shell">
      <Sidebar
        activeItem={activeItem}
        onSelect={handleSidebarSelect}
        reportsCount={results.length}
      />

      <main className="app-main">
        <section className="hero-panel" id="dashboard-section">
          <div className="hero-copy">
            <div className="hero-icon" aria-hidden="true">
              <GraduationCap size={28} />
            </div>
            <div>
              <p className="eyebrow">Academic code review</p>
              <h1>Astra Similarity Checker</h1>
              <p>
                Upload Python files and check structural similarity across
                student submissions.
              </p>
            </div>
          </div>
          <div className="hero-status">
            <div>
              <span>Ready for review</span>
              <strong>{flaggedCount} flagged</strong>
            </div>
            {flaggedCount > 0 ? (
              <AlertCircle size={24} />
            ) : (
              <CheckCircle2 size={24} />
            )}
          </div>
        </section>

        <div className="workspace-grid">
          <FileUpload
            files={files}
            isReading={isReadingFiles}
            notice={notice}
            onFilesAdded={handleFilesAdded}
            onRemoveFile={handleRemoveFile}
          />

          <AnalysisSettings
            files={files}
            comparisonMode={comparisonMode}
            threshold={threshold}
            referenceFileId={referenceFileId}
            isAnalyzing={isAnalyzing}
            onModeChange={setComparisonMode}
            onThresholdChange={setThreshold}
            onReferenceFileChange={setReferenceFileId}
            onStart={handleStartAnalysis}
          />
        </div>

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

        <ResultsTable
          results={results}
          threshold={threshold}
          onViewDetails={setSelectedResult}
        />

        <section className="integration-strip" aria-label="Prepared API payload">
          <div>
            <p className="eyebrow">Backend handoff</p>
            <strong>
              {lastPayload
                ? `${lastPayload.units.length} units prepared for /analyze`
                : "No payload prepared yet"}
            </strong>
          </div>
          <span>
            Mode: {comparisonMode === "all_pairs" ? "all_pairs" : "reference_file"}
          </span>
        </section>

        <ProjectInfo />
      </main>
    </div>
  );
}

function scrollToSection(item: SidebarItem) {
  document
    .getElementById(sectionIds[item])
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

export default App;
