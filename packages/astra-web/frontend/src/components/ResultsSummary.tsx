import { Card, CardContent } from "@/components/ui/card";
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
    <div className="grid grid-cols-2 gap-2 sm:grid-cols-4" aria-label="Analysis summary">
      {metrics.map((metric) => (
        <Card key={metric.label}>
          <CardContent className="p-3">
            <p className="text-sm text-muted-foreground">{metric.label}</p>
            <strong className="mt-1 block text-2xl leading-none font-semibold">
              {metric.value}
            </strong>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
