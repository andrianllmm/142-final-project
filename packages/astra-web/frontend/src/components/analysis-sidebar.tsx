import { Eye, Play, ShieldCheck } from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";
import { Slider } from "@/components/ui/slider";
import { cn } from "@/lib/utils";
import { SimilarityResult, SimilarityStatus } from "@/types";

interface AnalysisSidebarProps extends React.ComponentProps<typeof Sidebar> {
  fileCount: number;
  threshold: number;
  isAnalyzing: boolean;
  comparisons: SimilarityResult[];
  selectedResultId: string | null;
  onThresholdChange: (threshold: number) => void;
  onStart: () => void;
  onViewDetails: (result: SimilarityResult) => void;
}

export function AnalysisSidebar({
  fileCount,
  threshold,
  isAnalyzing,
  comparisons,
  selectedResultId,
  onThresholdChange,
  onStart,
  onViewDetails,
  ...props
}: AnalysisSidebarProps) {
  const canStart = fileCount >= 2 && !isAnalyzing;
  const highestScore = comparisons.reduce(
    (highest, result) => Math.max(highest, result.score),
    0,
  );
  const flaggedComparisons = comparisons.filter(
    (result) => result.score >= threshold,
  );

  const metrics = [
    { label: "Files", value: fileCount.toString() },
    { label: "Pairs", value: comparisons.length.toString() },
    { label: "Flagged", value: flaggedComparisons.length.toString() },
    { label: "Highest", value: `${Math.round(highestScore * 100)}%` },
  ];

  return (
    <Sidebar collapsible="offcanvas" side="right" {...props}>
      <SidebarHeader className="gap-4 border-b px-4 py-4">
        <Button
          size="lg"
          className="w-full"
          disabled={!canStart}
          onClick={onStart}
        >
          <Play size={16} fill="currentColor" />
          {isAnalyzing ? "Checking..." : "Compare all pairs"}
        </Button>

        <div className="grid gap-3">
          <div className="flex items-center justify-between">
            <Label htmlFor="threshold-range" className="text-sm font-medium">
              Flag threshold
            </Label>
            <div className="flex items-center gap-1.5 rounded-md border border-input bg-background px-2">
              <Input
                id="threshold-number"
                className="h-8 w-[3ch] border-0 bg-transparent px-0 text-right text-sm tabular-nums shadow-none focus-visible:ring-0 dark:bg-transparent"
                type="text"
                inputMode="numeric"
                pattern="[0-9]*"
                value={Math.round(threshold * 100)}
                onChange={(event) => {
                  const digitsOnly = event.target.value.replace(/[^0-9]/g, "");
                  onThresholdChange(
                    clampThreshold(Number(digitsOnly || 0) / 100),
                  );
                }}
                aria-label="Similarity threshold percentage"
              />
              <span className="text-sm text-muted-foreground">%</span>
            </div>
          </div>
          <Slider
            id="threshold-range"
            min={0}
            max={1}
            step={0.01}
            value={[threshold]}
            onValueChange={(value) =>
              onThresholdChange(Array.isArray(value) ? value[0] : value)
            }
          />
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Summary</SidebarGroupLabel>
          <SidebarGroupContent className="grid grid-cols-2 gap-2 px-1">
            {metrics.map((metric) => (
              <div
                key={metric.label}
                className="rounded-lg border border-sidebar-border px-2.5 py-2"
              >
                <p className="text-xs text-muted-foreground">{metric.label}</p>
                <strong className="mt-0.5 block text-lg leading-none font-semibold">
                  {metric.value}
                </strong>
              </div>
            ))}
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel>
            Similarity report
            {comparisons.length > 0 ? (
              <Badge variant="secondary" className="ml-auto">
                {Math.round(threshold * 100)}%
              </Badge>
            ) : null}
          </SidebarGroupLabel>
          <SidebarGroupContent>
            {comparisons.length === 0 ? (
              <div className="grid gap-2 px-3 py-6 text-center">
                <ShieldCheck
                  className="mx-auto text-muted-foreground"
                  size={24}
                />
                <p className="text-xs text-muted-foreground">
                  Upload at least two files and run a similarity check.
                </p>
              </div>
            ) : flaggedComparisons.length === 0 ? (
              <div className="grid gap-2 px-3 py-6 text-center">
                <ShieldCheck
                  className="mx-auto text-muted-foreground"
                  size={24}
                />
                <p className="text-xs text-muted-foreground">
                  No pairs meet the {Math.round(threshold * 100)}% threshold.
                </p>
              </div>
            ) : (
              <div className="grid gap-2">
                {flaggedComparisons.map((result) => (
                  <button
                    type="button"
                    key={result.id}
                    onClick={() => onViewDetails(result)}
                    className={cn(
                      "rounded-lg border border-sidebar-border p-2.5 text-left transition-colors hover:bg-sidebar-accent",
                      selectedResultId === result.id &&
                        "border-sidebar-ring bg-sidebar-accent",
                    )}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="min-w-0 truncate text-xs text-muted-foreground">
                        {result.fileA.name}
                      </span>
                      <Eye
                        size={13}
                        className="shrink-0 text-muted-foreground"
                      />
                    </div>
                    <div className="truncate text-xs text-muted-foreground">
                      vs {result.fileB.name}
                    </div>
                    <div className="mt-2 flex items-center gap-2">
                      <Progress
                        value={Math.round(result.score * 100)}
                        className={cn(
                          "w-full **:data-[slot=progress-track]:h-1.5",
                          statusIndicatorClass[result.status],
                        )}
                      />
                      <span className="w-9 shrink-0 text-right text-xs font-semibold">
                        {Math.round(result.score * 100)}%
                      </span>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarRail />
    </Sidebar>
  );
}

const statusIndicatorClass: Record<SimilarityStatus, string> = {
  low: "**:data-[slot=progress-indicator]:bg-emerald-500",
  medium: "**:data-[slot=progress-indicator]:bg-amber-500",
  high: "**:data-[slot=progress-indicator]:bg-destructive",
};

function clampThreshold(value: number): number {
  if (Number.isNaN(value)) {
    return 0;
  }

  return Math.min(1, Math.max(0, value));
}
