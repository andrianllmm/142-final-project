import { buildAnalysisPayload, getStatus } from "./mockAnalysis";
import {
  AnalysisPayload,
  ComparisonMode,
  SimilarityResult,
  UploadedCodeFile
} from "../types";

interface AnalyzeInput {
  files: UploadedCodeFile[];
  threshold: number;
  comparisonMode: ComparisonMode;
  referenceFileId?: string;
}

interface AnalyzeOutput {
  payload: AnalysisPayload;
  results: SimilarityResult[];
  message: string;
}

interface BackendAnalysisReport {
  threshold: number;
  total_units: number;
  scores: BackendSimilarityScore[];
  flagged_pairs: BackendSimilarityScore[];
  metadata: Record<string, unknown>;
}

interface BackendSimilarityScore {
  unit_a: string;
  unit_b: string;
  score: number;
  evidence?: BackendAlignment[];
}

interface BackendAlignment {
  left_chunk_index: number;
  right_chunk_index: number;
  similarity: number;
  left_start_line?: number;
  left_end_line?: number;
  right_start_line?: number;
  right_end_line?: number;
}

const API_BASE = (import.meta.env.VITE_ASTRA_API_BASE ?? "/api").replace(
  /\/$/,
  ""
);

export async function analyzeCodeSimilarity(
  input: AnalyzeInput
): Promise<AnalyzeOutput> {
  const payload = buildAnalysisPayload(input);

  try {
    const response = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "true"
      },
      body: JSON.stringify({
        units: payload.units,
        threshold: payload.threshold
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || `Backend returned ${response.status}`);
    }

    const report = (await response.json()) as BackendAnalysisReport;

    return {
      payload,
      results: mapBackendReport(report, input),
      message: `Backend analysis complete. ${report.scores.length} comparisons returned.`
    };
  } catch (error) {
    const reason = error instanceof Error ? error.message : "Unknown backend error";

    return {
      payload,
      results: [],
      message: `Backend analysis failed. ${reason}`
    };
  }
}

function mapBackendReport(
  report: BackendAnalysisReport,
  input: AnalyzeInput
): SimilarityResult[] {
  const filesById = new Map(input.files.map((file) => [file.id, file]));

  return report.scores
    .filter((score) =>
      input.comparisonMode === "reference_file" && input.referenceFileId
        ? score.unit_a === input.referenceFileId ||
          score.unit_b === input.referenceFileId
        : true
    )
    .map((score) => {
      const fileA = filesById.get(score.unit_a);
      const fileB = filesById.get(score.unit_b);

      if (!fileA || !fileB) {
        return null;
      }

      return {
        id: `${score.unit_a}:${score.unit_b}`,
        fileA,
        fileB,
        score: clampScore(score.score),
        status: getStatus(score.score),
        highlights: highlightsFromEvidence(score.evidence, fileA, fileB),
        findings: [
          "Possible copied structure",
          "Similar function names",
          "Similar logic blocks"
        ]
      };
    })
    .filter((result): result is SimilarityResult => Boolean(result))
    .sort((left, right) => right.score - left.score);
}

function clampScore(score: number): number {
  return Math.min(1, Math.max(0, score));
}

function highlightsFromEvidence(
  evidence: BackendAlignment[] | undefined,
  fileA: UploadedCodeFile,
  fileB: UploadedCodeFile
): { left: number[]; right: number[] } {
  if (evidence && evidence.length > 0) {
    const relevantEvidence = evidence
      .filter((item) => item.similarity >= 0.55)
      .slice(0, 6);

    return {
      left: uniqueLines(
        relevantEvidence.flatMap((item) =>
          lineRange(
            item.left_start_line ?? item.left_chunk_index + 1,
            item.left_end_line ?? item.left_chunk_index + 1,
            fileA
          )
        )
      ),
      right: uniqueLines(
        relevantEvidence.flatMap((item) =>
          lineRange(
            item.right_start_line ?? item.right_chunk_index + 1,
            item.right_end_line ?? item.right_chunk_index + 1,
            fileB
          )
        )
      )
    };
  }

  return {
    left: [2, 3, 4].map((line) => limitLine(line, fileA)),
    right: [2, 3, 4].map((line) => limitLine(line, fileB))
  };
}

function limitLine(line: number, file: UploadedCodeFile): number {
  const lineCount = Math.max(file.content.split(/\r?\n/).length, 1);

  return Math.min(Math.max(line, 1), lineCount);
}

function lineRange(
  startLine: number,
  endLine: number,
  file: UploadedCodeFile
): number[] {
  const start = limitLine(startLine, file);
  const end = limitLine(Math.max(startLine, endLine), file);

  return Array.from({ length: end - start + 1 }, (_, index) => start + index);
}

function uniqueLines(lines: number[]): number[] {
  return [...new Set(lines)].sort((left, right) => left - right);
}
