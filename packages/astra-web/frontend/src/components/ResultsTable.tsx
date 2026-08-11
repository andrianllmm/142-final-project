import { Eye, ShieldCheck } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { cn } from "@/lib/utils";
import { SimilarityResult, SimilarityStatus } from "../types";

interface ResultsTableProps {
  results: SimilarityResult[];
  threshold: number;
  onViewDetails: (result: SimilarityResult) => void;
}

export function ResultsTable({
  results,
  threshold,
  onViewDetails,
}: ResultsTableProps) {
  return (
    <Card id="reports-section" className="overflow-hidden">
      <CardHeader className="flex-row items-start justify-between gap-3">
        <CardTitle>Similarity Report</CardTitle>
        <Badge variant="secondary">
          Flag threshold {Math.round(threshold * 100)}%
        </Badge>
      </CardHeader>
      <CardContent>
        {results.length === 0 ? (
          <div className="grid min-h-56 place-items-center gap-2 rounded-lg border bg-muted/30 p-6 text-center">
            <ShieldCheck className="text-muted-foreground" size={32} />
            <h3 className="font-semibold">No report generated yet</h3>
            <p className="text-sm text-muted-foreground">
              Upload at least two supported files and start a similarity check.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <Table className="min-w-[780px]">
              <TableHeader>
                <TableRow>
                  <TableHead>File A</TableHead>
                  <TableHead>File B</TableHead>
                  <TableHead>Similarity Score</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {results.map((result) => (
                  <TableRow key={result.id}>
                    <TableCell>{result.fileA.name}</TableCell>
                    <TableCell>{result.fileB.name}</TableCell>
                    <TableCell>
                      <div className="grid min-w-[155px] gap-1.5">
                        <span className="font-semibold">
                          {Math.round(result.score * 100)}%
                        </span>
                        <Progress
                          value={Math.round(result.score * 100)}
                          className={cn(
                            "h-1.5",
                            statusIndicatorClass[result.status],
                          )}
                        />
                      </div>
                    </TableCell>
                    <TableCell>
                      <StatusBadge status={result.status} />
                    </TableCell>
                    <TableCell>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => onViewDetails(result)}
                      >
                        <Eye size={16} />
                        View Details
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

const statusIndicatorClass: Record<SimilarityStatus, string> = {
  low: "[&>div]:bg-emerald-500",
  medium: "[&>div]:bg-amber-500",
  high: "[&>div]:bg-destructive",
};

const statusBadgeVariant: Record<
  SimilarityStatus,
  "secondary" | "outline" | "destructive"
> = {
  low: "secondary",
  medium: "outline",
  high: "destructive",
};

export function StatusBadge({ status }: { status: SimilarityStatus }) {
  const label =
    status === "high"
      ? "High similarity"
      : status === "medium"
        ? "Medium similarity"
        : "Low similarity";

  return <Badge variant={statusBadgeVariant[status]}>{label}</Badge>;
}
