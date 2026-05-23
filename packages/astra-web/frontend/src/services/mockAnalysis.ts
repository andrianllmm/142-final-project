import {
  AnalysisPayload,
  ComparisonMode,
  SimilarityResult,
  SimilarityStatus,
  UploadedCodeFile
} from "../types";

export const SUPPORTED_EXTENSIONS = [".py"];

interface MockAnalysisInput {
  files: UploadedCodeFile[];
  threshold: number;
  comparisonMode: ComparisonMode;
  referenceFileId?: string;
}

export function buildAnalysisPayload({
  files,
  threshold,
  comparisonMode,
  referenceFileId
}: MockAnalysisInput): AnalysisPayload {
  return {
    units: files.map((file) => ({
      id: file.id,
      content: file.content
    })),
    threshold,
    comparisonMode,
    ...(comparisonMode === "reference_file" && referenceFileId
      ? { referenceFileId }
      : {})
  };
}

export function createMockResults({
  files,
  comparisonMode,
  referenceFileId
}: MockAnalysisInput): SimilarityResult[] {
  const pairs = getComparisonPairs(files, comparisonMode, referenceFileId);

  return pairs
    .map(([fileA, fileB]) => {
      const score = deterministicScore(fileA, fileB);

      return {
        id: `${fileA.id}:${fileB.id}`,
        fileA,
        fileB,
        score,
        status: getStatus(score),
        highlights: buildHighlights(fileA, fileB, score),
        findings: [
          "Possible copied structure",
          "Similar function names",
          "Similar logic blocks"
        ]
      };
    })
    .sort((left, right) => right.score - left.score);
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

function getComparisonPairs(
  files: UploadedCodeFile[],
  comparisonMode: ComparisonMode,
  referenceFileId?: string
): Array<[UploadedCodeFile, UploadedCodeFile]> {
  if (comparisonMode === "reference_file") {
    const referenceFile = files.find((file) => file.id === referenceFileId);
    if (!referenceFile) {
      return [];
    }

    return files
      .filter((file) => file.id !== referenceFile.id)
      .map((file) => [referenceFile, file]);
  }

  const pairs: Array<[UploadedCodeFile, UploadedCodeFile]> = [];
  for (let leftIndex = 0; leftIndex < files.length; leftIndex += 1) {
    for (
      let rightIndex = leftIndex + 1;
      rightIndex < files.length;
      rightIndex += 1
    ) {
      pairs.push([files[leftIndex], files[rightIndex]]);
    }
  }

  return pairs;
}

function deterministicScore(
  fileA: UploadedCodeFile,
  fileB: UploadedCodeFile
): number {
  const normalizedContentA = stripComments(fileA.content);
  const normalizedContentB = stripComments(fileB.content);
  const sharedWords = sharedWordCount(normalizedContentA, normalizedContentB);
  const key = [
    fileA.name,
    fileB.name,
    normalizedContentA.length,
    normalizedContentB.length,
    sharedWords
  ].join("|");

  let hash = 0;
  for (let index = 0; index < key.length; index += 1) {
    hash = (hash * 31 + key.charCodeAt(index)) % 100000;
  }

  const structuralLift =
    fileA.extension === fileB.extension ? 0.14 : fileA.type === fileB.type ? 0.07 : 0;
  const sharedLift = Math.min(sharedWords / 140, 0.18);
  const base = 0.34 + (hash % 42) / 100;

  return Math.min(0.97, Number((base + structuralLift + sharedLift).toFixed(2)));
}

function stripComments(source: string): string {
  return source
    .replace(/<!--[\s\S]*?-->/g, " ")
    .replace(/\/\*[\s\S]*?\*\//g, " ")
    .split(/\r?\n/)
    .map((line) => line.replace(/(^|\s)(#|\/\/).*$/, "$1"))
    .join("\n");
}

function sharedWordCount(left: string, right: string): number {
  const tokenize = (value: string) =>
    new Set(value.toLowerCase().match(/[a-z_][a-z0-9_]*/g) ?? []);
  const leftTokens = tokenize(left);
  const rightTokens = tokenize(right);

  let shared = 0;
  leftTokens.forEach((token) => {
    if (rightTokens.has(token)) {
      shared += 1;
    }
  });

  return shared;
}

function buildHighlights(
  fileA: UploadedCodeFile,
  fileB: UploadedCodeFile,
  score: number
): { left: number[]; right: number[] } {
  const leftLineCount = Math.max(fileA.content.split(/\r?\n/).length, 8);
  const rightLineCount = Math.max(fileB.content.split(/\r?\n/).length, 8);
  const span = score >= 0.8 ? 5 : score >= 0.55 ? 3 : 2;

  return {
    left: Array.from({ length: span }, (_, index) =>
      Math.min(leftLineCount, index + 2)
    ),
    right: Array.from({ length: span }, (_, index) =>
      Math.min(rightLineCount, index + 2)
    )
  };
}
