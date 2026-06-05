import { ChangeEvent, DragEvent, useRef, useState } from "react";
import { Edit3, FileCode2, Trash2, UploadCloud } from "lucide-react";
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
    <section className="panel upload-panel" id="new-analysis-section">
      <div className="section-heading">
        <div>
          <h2>Files</h2>
        </div>
        <span className="soft-badge">{files.length} files</span>
      </div>

      <div
        className={`dropzone ${isDragging ? "is-dragging" : ""}`}
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
          className="visually-hidden"
          type="file"
          multiple
          accept={SUPPORTED_EXTENSIONS.join(",")}
          onChange={handleInputChange}
        />
        <div className="dropzone-icon">
          <UploadCloud size={28} />
        </div>
        <h3>Drop Python files here</h3>
        <p>or browse</p>
        <div className="format-row" aria-label="Supported formats">
          {SUPPORTED_EXTENSIONS.map((extension) => (
            <span key={extension}>{extension}</span>
          ))}
        </div>
      </div>

      <div className="upload-meta" aria-live="polite">
        {isReading ? "Reading file contents..." : notice}
      </div>

      <div className="file-list" aria-label="Uploaded files">
        {files.length === 0 ? (
          <div className="empty-list">No Python files uploaded yet.</div>
        ) : (
          files.map((file) => (
            <div className="file-row" key={file.id}>
              <div className="file-icon" aria-hidden="true">
                <FileCode2 size={18} />
              </div>
              <div className="file-main">
                <strong>{file.name}</strong>
                <span>{file.type}</span>
              </div>
              <span className="file-size">{formatBytes(file.size)}</span>
              <button
                className="icon-button"
                type="button"
                aria-label={`View or edit ${file.name}`}
                onClick={() => onEditFile(file.id)}
              >
                <Edit3 size={16} />
              </button>
              <button
                className="icon-button"
                type="button"
                aria-label={`Remove ${file.name}`}
                onClick={() => onRemoveFile(file.id)}
              >
                <Trash2 size={17} />
              </button>
            </div>
          ))
        )}
      </div>
    </section>
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
