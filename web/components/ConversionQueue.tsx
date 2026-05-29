"use client";

import FormatSelector from "./FormatSelector";
import ProgressBar from "./ProgressBar";
import FileChip from "./ui/FileChip";

export type QueuedFile = {
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
  onUpdateTarget: (index: number, targetExt: string) => void;
  onRemove: (index: number) => void;
  onConvertAll: () => void;
};

export default function ConversionQueue({ queue, onUpdateTarget, onRemove, onConvertAll }: Props) {
  const isConverting = queue.some(q => q.status === "converting");

  return (
    <div className="glass-card rounded-xl p-md flex flex-col gap-sm">
      <div className="flex items-center justify-between">
        <p className="text-label-md text-on-surface-variant uppercase tracking-wider">
          Queue ({queue.length})
        </p>
        <button 
          className="glass-button-primary text-label-md disabled:opacity-50 disabled:cursor-not-allowed" 
          onClick={onConvertAll}
          disabled={isConverting || queue.every(q => q.status === "done" || !q.targetExt)}
        >
          {isConverting ? "Converting..." : "Convert All"}
          <span className="material-symbols-outlined text-base ml-xs align-middle">
            arrow_forward
          </span>
        </button>
      </div>

      {queue.map((item, i) => (
        <div
          key={i}
          className="glass-card rounded-lg p-sm flex items-center gap-sm"
        >
          {/* File type chip */}
          <FileChip ext={item.sourceExt} status={item.status} />

          {/* File name + progress */}
          <div className="flex-grow min-w-0">
            <p className="text-body-md text-on-surface truncate">{item.file.name}</p>
            <p className="text-label-sm text-outline">
              {(item.file.size / 1024).toFixed(0)} KB
            </p>
            {item.status === "converting" && (
              <ProgressBar value={item.progress ?? 0} />
            )}
            {item.status === "done" && (
              <p className="text-label-sm text-tertiary mt-xs">
                ✓ Ready to download
              </p>
            )}
            {item.status === "error" && (
              <p className="text-label-sm text-error mt-xs">{item.error}</p>
            )}
          </div>

          {/* Format selector */}
          {item.status === "pending" && (
            <FormatSelector
              sourceExt={item.sourceExt}
              value={item.targetExt}
              onChange={(ext) => onUpdateTarget(i, ext)}
            />
          )}

          {/* Download or close */}
          {item.status === "done" && item.resultUrl ? (
            <a
              href={item.resultUrl}
              download={item.file.name.replace(`.${item.sourceExt}`, `.${item.targetExt}`)}
              className="glass-button-primary text-label-md text-center"
            >
              Download
            </a>
          ) : (
            <button
              className="text-outline hover:text-error transition-colors ml-2"
              onClick={() => onRemove(i)}
              disabled={item.status === "converting"}
            >
              <span className="material-symbols-outlined text-base">close</span>
            </button>
          )}
        </div>
      ))}
    </div>
  );
}
