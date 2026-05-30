"use client";
import FileChip from "./ui/FileChip";
import FormatSelector from "./FormatSelector";
import ProgressBar from "./ProgressBar";

export type QueuedFile = {
  id: string;
  file: File;
  sourceExt: string;
  targetExt: string;
  status: "pending" | "converting" | "done" | "error";
  progress?: number;
  resultUrl?: string;
  error?: string;
};

type Props = {
  queue: QueuedFile[];
  onUpdateTarget: (id: string, ext: string) => void;
  onRemove: (id: string) => void;
  onConvertAll: () => void;
};

function formatBytes(n: number): string {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(0)} KB`;
  return `${(n / (1024 * 1024)).toFixed(1)} MB`;
}

export default function ConversionQueue({ queue, onUpdateTarget, onRemove, onConvertAll }: Props) {
  const pendingWithTarget = queue.filter(q => q.status === "pending" && q.targetExt);
  const allDone = queue.length > 0 && queue.every(q => q.status === "done");

  return (
    <div className="glass-card rounded-xl p-md flex flex-col gap-sm">
      {/* Header */}
      <div className="flex items-center justify-between">
        <span className="text-label-md text-outline uppercase tracking-wider">
          Queue ({queue.length})
        </span>
        {!allDone && pendingWithTarget.length > 0 && (
          <button className="glass-button-primary text-label-md" onClick={onConvertAll}>
            Convert All
            <span className="material-symbols-outlined" style={{ fontSize: 16 }}>arrow_forward</span>
          </button>
        )}
      </div>

      {/* Rows */}
      {queue.map((item) => (
        <div key={item.id} className="flex items-center gap-sm p-sm rounded-lg border border-outline-variant/20 bg-surface-container/40">
          {/* Badge */}
          <FileChip ext={item.sourceExt} status={item.status} />

          {/* Info */}
          <div className="flex-grow min-w-0">
            <p className="text-body-md text-on-surface truncate font-medium">{item.file.name}</p>
            <p className="text-label-sm text-outline">{formatBytes(item.file.size)}</p>

            {item.status === "converting" && (
              <ProgressBar value={item.progress ?? 20} />
            )}
            {item.status === "done" && (
              <p className="text-label-sm text-tertiary mt-0.5">✓ Ready to download</p>
            )}
            {item.status === "error" && (
              <p className="text-label-sm text-error mt-0.5 truncate">{item.error}</p>
            )}
          </div>

          {/* Format selector or arrow */}
          {item.status === "pending" && (
            <FormatSelector
              sourceExt={item.sourceExt}
              value={item.targetExt}
              onChange={(ext) => onUpdateTarget(item.id, ext)}
            />
          )}

          {/* Download or remove */}
          {item.status === "done" && item.resultUrl ? (
            <a
              href={item.resultUrl}
              download={`${item.file.name.replace(/\.[^.]+$/, "")}.${item.targetExt}`}
              className="glass-button-primary text-label-md flex-shrink-0"
            >
              <span className="material-symbols-outlined" style={{ fontSize: 16 }}>download</span>
              Save
            </a>
          ) : (
            <button
              onClick={() => onRemove(item.id)}
              className="text-outline hover:text-error transition-colors p-1 flex-shrink-0"
              title="Remove"
            >
              <span className="material-symbols-outlined" style={{ fontSize: 18 }}>close</span>
            </button>
          )}
        </div>
      ))}
    </div>
  );
}
