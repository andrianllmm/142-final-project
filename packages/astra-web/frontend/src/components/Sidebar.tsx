import {
  BarChart3,
  BookOpenText,
  FileText,
  LayoutDashboard,
  Settings,
  Sparkles,
  UploadCloud
} from "lucide-react";

type SidebarItem =
  | "dashboard"
  | "new-analysis"
  | "reports"
  | "settings"
  | "project-info";

interface SidebarProps {
  activeItem: SidebarItem;
  onSelect: (item: SidebarItem) => void;
  reportsCount: number;
}

const sidebarItems = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "new-analysis", label: "New Analysis", icon: UploadCloud },
  { id: "reports", label: "Reports", icon: FileText },
  { id: "settings", label: "Settings", icon: Settings },
  { id: "project-info", label: "Project Info", icon: BookOpenText }
] as const;

export function Sidebar({ activeItem, onSelect, reportsCount }: SidebarProps) {
  return (
    <aside className="sidebar" aria-label="Primary navigation">
      <div className="brand-block">
        <div className="brand-mark" aria-hidden="true">
          <Sparkles size={21} strokeWidth={2.4} />
        </div>
        <div>
          <p className="brand-kicker">Astra</p>
          <p className="brand-title">Similarity Checker</p>
        </div>
      </div>

      <nav className="sidebar-nav">
        {sidebarItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeItem === item.id;

          return (
            <button
              className={`nav-item ${isActive ? "is-active" : ""}`}
              key={item.id}
              onClick={() => onSelect(item.id)}
              type="button"
            >
              <Icon size={18} />
              <span>{item.label}</span>
              {item.id === "reports" && reportsCount > 0 ? (
                <span className="nav-count">{reportsCount}</span>
              ) : null}
            </button>
          );
        })}
      </nav>

      <div className="sidebar-foot">
        <BarChart3 size={18} />
        <div>
          <p>Academic review</p>
          <span>Python AST similarity</span>
        </div>
      </div>
    </aside>
  );
}
