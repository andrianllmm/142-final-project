import { SimilarityResult } from "../types";

interface ResultsSummaryProps {
  totalFiles: number;
  threshold: number;
  results: SimilarityResult[];
}

export function ResultsSummary({
  totalFiles,
  threshold,
  results,
}: ResultsSummaryProps) {
  const highestScore = results.reduce(
    (highest, result) => Math.max(highest, result.score),
    0,
  );
  const flaggedCount = results.filter(
    (result) => result.score >= threshold,
  ).length;
  const metrics = [
    {
      label: "Files",
      value: totalFiles.toString(),
    },
    {
      label: "Pairs",
      value: results.length.toString(),
    },
    {
      label: "Flagged",
      value: flaggedCount.toString(),
    },
    {
      label: "Highest",
      value: `${Math.round(highestScore * 100)}%`,
    },
  ];

  return (
    <div className="summary-grid" aria-label="Analysis summary">
      {metrics.map((metric) => (
        <article className="summary-card" key={metric.label}>
          <p>{metric.label}</p>
          <strong>{metric.value}</strong>
        </article>
      ))}
    </div>
  );
}
