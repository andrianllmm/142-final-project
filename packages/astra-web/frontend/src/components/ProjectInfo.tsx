import { BookOpenText, Database, GitCompareArrows, UsersRound } from "lucide-react";

const references = [
  "https://doi.org/10.3390/app132011358",
  "https://doi.org/10.1145/3313290",
  "https://doi.org/10.15294/sji.v11i1.48064",
  "https://ceur-ws.org/Vol-2259/aics_33.pdf",
  "https://yangdanny97.github.io/blog/2019/05/03/MOSS",
  "https://glotta.ntua.gr/IS-Social/CopyRight/Plagiarism%20Detection.htm",
  "https://jplag.github.io/Demo/overview"
];

export function ProjectInfo() {
  return (
    <section className="panel project-panel" id="project-info-section">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Project info</p>
          <h2>Astra: Code Plagiarism Detector for Programming Assignments</h2>
        </div>
        <span className="soft-badge">CMSC 142</span>
      </div>

      <div className="project-lead">
        <div>
          <p className="project-label">Internal Code Similarity Detection System</p>
          <h3>
            Student programming submissions using AST normalization and
            Damerau-Levenshtein sequence alignment
          </h3>
          <p>
            Astra helps instructors rank suspicious Python submission pairs by
            comparing normalized program structure instead of raw source text.
          </p>
        </div>
        <div className="project-team">
          <UsersRound size={20} />
          <div>
            <strong>Group Members</strong>
            <span>Andrian Lloyd Maagma</span>
            <span>Dejel Cyrus De Asis</span>
            <span>John Romyr Lopez</span>
          </div>
        </div>
      </div>

      <div className="project-grid">
        <article>
          <GitCompareArrows size={20} />
          <h3>Algorithm</h3>
          <p>
            Python files are parsed into ASTs, normalized to remove superficial
            differences, chunked structurally, and compared with
            Damerau-Levenshtein dynamic programming.
          </p>
        </article>
        <article>
          <Database size={20} />
          <h3>Outputs</h3>
          <p>
            The system returns pairwise similarity scores, ranked suspicious
            pairs, threshold-based flags, and chunk-level evidence for review.
          </p>
        </article>
        <article>
          <BookOpenText size={20} />
          <h3>Scope</h3>
          <p>
            Designed exclusively for single-file Python lab submissions and
            small to medium class batches of about 15 to 30 students.
          </p>
        </article>
      </div>

      <div className="project-columns">
        <div>
          <h3>System Design Flow</h3>
          <ul className="compact-list">
            <li>Load Python source files or folders.</li>
            <li>Parse, normalize, and remove docstrings/comments.</li>
            <li>Extract structural chunks and preorder token sequences.</li>
            <li>Compare chunk pairs with Damerau-Levenshtein distance.</li>
            <li>Aggregate scores, rank pairs, and flag threshold matches.</li>
          </ul>
        </div>
        <div>
          <h3>Limitations</h3>
          <ul className="compact-list">
            <li>Python `.py` submissions only.</li>
            <li>Focused on syntactic and structural similarity.</li>
            <li>Does not prove semantic equivalence or plagiarism intent.</li>
            <li>Pairwise comparison has O(n^2) scaling.</li>
          </ul>
        </div>
      </div>

      <div className="reference-list">
        <h3>References</h3>
        <div>
          {references.map((reference) => (
            <a key={reference} href={reference} target="_blank" rel="noreferrer">
              {reference}
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}
