import { ChangeEvent, DragEvent, useRef, useState } from "react";
import { FileCode2, Trash2, Upload } from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupAction,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuAction,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/components/ui/sidebar";
import { cn } from "@/lib/utils";
import { SUPPORTED_EXTENSIONS } from "@/services/analysisUtils";
import { UploadedCodeFile } from "@/types";

interface AppSidebarProps extends React.ComponentProps<typeof Sidebar> {
  files: UploadedCodeFile[];
  activeFileId: string;
  notice: string;
  isReading: boolean;
  onFilesAdded: (files: File[]) => void;
  onSelectFile: (fileId: string) => void;
  onRemoveFile: (fileId: string) => void;
}

export function AppSidebar({
  files,
  activeFileId,
  notice,
  isReading,
  onFilesAdded,
  onSelectFile,
  onRemoveFile,
  ...props
}: AppSidebarProps) {
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
    <Sidebar collapsible="offcanvas" {...props}>
      <SidebarHeader className="border-b px-3 py-2.5">
        <span className="px-1 text-sm font-semibold tracking-tight">
          Astra
        </span>
        <span className="px-1 text-xs text-muted-foreground">
          Similarity checker
        </span>
      </SidebarHeader>
      <SidebarContent
        onDragEnter={(event) => {
          event.preventDefault();
          setIsDragging(true);
        }}
        onDragOver={(event) => event.preventDefault()}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={cn(
          "transition-colors",
          isDragging && "bg-sidebar-accent/60",
        )}
      >
        <input
          ref={inputRef}
          className="sr-only"
          type="file"
          multiple
          accept={SUPPORTED_EXTENSIONS.join(",")}
          onChange={handleInputChange}
        />
        <SidebarGroup>
          <SidebarGroupLabel>Files</SidebarGroupLabel>
          <SidebarGroupAction
            title="Upload files"
            aria-label="Upload files"
            onClick={() => inputRef.current?.click()}
          >
            <Upload />
          </SidebarGroupAction>
          <SidebarGroupContent>
            {files.length === 0 ? (
              <button
                type="button"
                onClick={() => inputRef.current?.click()}
                className="flex w-full flex-col items-center gap-1.5 rounded-lg border border-dashed border-sidebar-border px-3 py-6 text-center text-xs text-muted-foreground transition-colors hover:border-sidebar-ring hover:text-sidebar-foreground"
              >
                <Upload size={16} />
                {isReading ? "Reading files..." : "Drop .py files or click"}
              </button>
            ) : (
              <SidebarMenu>
                {files.map((file) => (
                  <SidebarMenuItem key={file.id}>
                    <SidebarMenuButton
                      isActive={file.id === activeFileId}
                      onClick={() => onSelectFile(file.id)}
                      className="pr-7"
                    >
                      <FileCode2 />
                      <span className="truncate">{file.name}</span>
                    </SidebarMenuButton>
                    <SidebarMenuAction
                      showOnHover
                      aria-label={`Remove ${file.name}`}
                      onClick={(event) => {
                        event.stopPropagation();
                        onRemoveFile(file.id);
                      }}
                    >
                      <Trash2 />
                    </SidebarMenuAction>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            )}
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <div className="border-t px-3 py-2 text-xs text-muted-foreground">
        {notice}
      </div>
      <SidebarRail />
    </Sidebar>
  );
}
