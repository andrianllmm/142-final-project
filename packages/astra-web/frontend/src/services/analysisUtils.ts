import { AnalysisPayload, SimilarityStatus, UploadedCodeFile } from "../types";

export const SUPPORTED_EXTENSIONS = [".py"];

interface AnalysisInput {
  files: UploadedCodeFile[];
  threshold: number;
}

export function buildAnalysisPayload({
  files,
  threshold,
}: AnalysisInput): AnalysisPayload {
  return {
    units: files.map((file) => ({
      id: file.id,
      content: file.content,
    })),
    threshold,
    comparisonMode: "all_pairs",
  };
}

export function getStatus(score: number): SimilarityStatus {
  if (score >= 0.8) {
    return "high";
  }

  if (score >= 0.55) {
    return "medium";
  }

  return "low";
}

export function getExtension(fileName: string): string {
  const dotIndex = fileName.lastIndexOf(".");
  return dotIndex >= 0 ? fileName.slice(dotIndex).toLowerCase() : "";
}

export function isSupportedFile(fileName: string): boolean {
  return SUPPORTED_EXTENSIONS.includes(getExtension(fileName));
}
