import { Play } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Slider } from "@/components/ui/slider";
import { UploadedCodeFile } from "../types";

interface AnalysisSettingsProps {
  files: UploadedCodeFile[];
  threshold: number;
  isAnalyzing: boolean;
  onThresholdChange: (threshold: number) => void;
  onStart: () => void;
}

export function AnalysisSettings({
  files,
  threshold,
  isAnalyzing,
  onThresholdChange,
  onStart,
}: AnalysisSettingsProps) {
  const canStart = files.length >= 2 && !isAnalyzing;

  return (
    <Card id="settings-section">
      <CardContent className="grid gap-4">
        <Button
          className="w-full"
          size="lg"
          disabled={!canStart || isAnalyzing}
          onClick={onStart}
        >
          <Play size={18} fill="currentColor" />
          {isAnalyzing ? "Checking..." : "Compare all pairs"}
        </Button>

        <div className="grid gap-2">
          <div className="flex items-center justify-between gap-3">
            <Label htmlFor="threshold-range">Flag threshold</Label>
            <Input
              id="threshold-number"
              className="w-20"
              type="number"
              min={0}
              max={1}
              step={0.01}
              value={threshold.toFixed(2)}
              onChange={(event) =>
                onThresholdChange(clampThreshold(Number(event.target.value)))
              }
              aria-label="Similarity threshold number"
            />
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
      </CardContent>
    </Card>
  );
}

function clampThreshold(value: number): number {
  if (Number.isNaN(value)) {
    return 0;
  }

  return Math.min(1, Math.max(0, value));
}
