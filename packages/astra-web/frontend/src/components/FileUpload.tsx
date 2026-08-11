import { ChangeEvent, DragEvent, useRef, useState } from "react";
import { Edit3, FileCode2, Trash2, UploadCloud } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { SUPPORTED_EXTENSIONS } from "../services/analysisUtils";
import { UploadedCodeFile } from "../types";

interface FileUploadProps {
  files: UploadedCodeFile[];
  isReading: boolean;
  notice: string;
  onFilesAdded: (files: File[]) => void;
  onEditFile: (fileId: string) => void;
  onRemoveFile: (fileId: string) => void;
}

export function FileUpload({
  files,
  isReading,
  notice,
  onFilesAdded,
  onEditFile,
  onRemoveFile,
}: FileUploadProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  function handleInputChange(event: ChangeEvent<HTMLInputElement>) {
    if (event.target.files) {
      onFilesAdded(Array.from(event.target.files));
      event.target.value = "";
    }
  }

  function handleDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setIsDragging(false);
    onFilesAdded(Array.from(event.dataTransfer.files));
  }

  return (
    <Card id="new-analysis-section">
      <CardHeader className="flex-row items-start justify-between gap-3">
        <CardTitle>Files</CardTitle>
        <Badge variant="secondary">{files.length} files</Badge>
      </CardHeader>
      <CardContent className="grid gap-4">
        <div
          className={cn(
            "grid min-h-40 place-items-center gap-2 rounded-lg border border-dashed border-input bg-muted/30 p-5 text-center transition-colors",
            isDragging && "border-primary bg-primary/5",
          )}
          onDragEnter={(event) => {
            event.preventDefault();
            setIsDragging(true);
          }}
          onDragOver={(event) => event.preventDefault()}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
          role="button"
          tabIndex={0}
          onClick={() => inputRef.current?.click()}
          onKeyDown={(event) => {
            if (event.key === "Enter" || event.key === " ") {
              inputRef.current?.click();
            }
          }}
        >
          <input
            ref={inputRef}
            className="sr-only"
            type="file"
            multiple
            accept={SUPPORTED_EXTENSIONS.join(",")}
            onChange={handleInputChange}
          />
          <div className="grid size-14 place-items-center rounded-lg bg-primary/10 text-primary">
            <UploadCloud size={26} />
          </div>
          <h3 className="text-base font-semibold">Drop Python files here</h3>
          <p className="text-sm text-muted-foreground">or browse</p>
          <div className="flex flex-wrap justify-center gap-1.5" aria-label="Supported formats">
            {SUPPORTED_EXTENSIONS.map((extension) => (
              <Badge variant="outline" key={extension}>
                {extension}
              </Badge>
            ))}
          </div>
        </div>

        <div className="min-h-5 text-sm text-muted-foreground" aria-live="polite">
          {isReading ? "Reading file contents..." : notice}
        </div>

        <div className="grid gap-2" aria-label="Uploaded files">
          {files.length === 0 ? (
            <div className="rounded-lg border bg-muted/30 p-4 text-center text-sm text-muted-foreground">
              No Python files uploaded yet.
            </div>
          ) : (
            files.map((file) => (
              <div
                className="grid grid-cols-[36px_minmax(0,1fr)_auto_auto_auto] items-center gap-2.5 rounded-lg border bg-background p-2.5"
                key={file.id}
              >
                <div className="grid size-9 place-items-center rounded-lg bg-primary/10 text-primary" aria-hidden="true">
                  <FileCode2 size={18} />
                </div>
                <div className="min-w-0">
                  <strong className="block truncate text-sm font-medium">
                    {file.name}
                  </strong>
                  <span className="block truncate text-xs text-muted-foreground">
                    {file.type}
                  </span>
                </div>
                <span className="text-xs text-muted-foreground">
                  {formatBytes(file.size)}
                </span>
                <Button
                  variant="outline"
                  size="icon-sm"
                  aria-label={`View or edit ${file.name}`}
                  onClick={() => onEditFile(file.id)}
                >
                  <Edit3 size={16} />
                </Button>
                <Button
                  variant="outline"
                  size="icon-sm"
                  aria-label={`Remove ${file.name}`}
                  onClick={() => onRemoveFile(file.id)}
                >
                  <Trash2 size={17} />
                </Button>
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) {
    return `${bytes} B`;
  }

  const kilobytes = bytes / 1024;
  if (kilobytes < 1024) {
    return `${kilobytes.toFixed(1)} KB`;
  }

  return `${(kilobytes / 1024).toFixed(1)} MB`;
}
