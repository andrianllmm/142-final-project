import { Eye, ShieldCheck } from "lucide-react";
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
    <section className="panel results-panel" id="reports-section">
      <div className="section-heading">
        <div>
          <h2>Similarity Report</h2>
        </div>
        <span className="soft-badge">
          Flag threshold {Math.round(threshold * 100)}%
        </span>
      </div>

      {results.length === 0 ? (
        <div className="empty-report">
          <ShieldCheck size={32} />
          <h3>No report generated yet</h3>
          <p>
            Upload at least two supported files and start a similarity check.
          </p>
        </div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>File A</th>
                <th>File B</th>
                <th>Similarity Score</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {results.map((result) => (
                <tr key={result.id}>
                  <td>{result.fileA.name}</td>
                  <td>{result.fileB.name}</td>
                  <td>
                    <div className="score-cell">
                      <span>{Math.round(result.score * 100)}%</span>
                      <div className="score-track" aria-hidden="true">
                        <div
                          className={`score-fill status-${result.status}`}
                          style={{
                            width: `${Math.round(result.score * 100)}%`,
                          }}
                        />
                      </div>
                    </div>
                  </td>
                  <td>
                    <StatusBadge status={result.status} />
                  </td>
                  <td>
                    <button
                      className="table-action"
                      type="button"
                      onClick={() => onViewDetails(result)}
                    >
                      <Eye size={16} />
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

export function StatusBadge({ status }: { status: SimilarityStatus }) {
  const label =
    status === "high"
      ? "High similarity"
      : status === "medium"
        ? "Medium similarity"
        : "Low similarity";

  return <span className={`status-badge status-${status}`}>{label}</span>;
}
