"use client";

import { useCallback, useRef, useState } from "react";
import { checkFileSizeLimit } from "@/lib/validate";
import { WEB_UNSUPPORTED_FORMATS, WEB_FILE_SIZE_LIMIT_LABEL } from "@/lib/constants";
import { convertFile } from "@/lib/api";
import DesktopCTA from "./DesktopCTA";
import ConversionQueue, { QueuedFile } from "./ConversionQueue";

export default function DropZone() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragActive, setDragActive] = useState(false);
  const [showSizeCTA, setShowSizeCTA] = useState(false);
  const [queue, setQueue] = useState<QueuedFile[]>([]);

  const addFiles = useCallback((files: FileList | File[]) => {
    const arr = Array.from(files);
    setShowSizeCTA(false);

    for (const file of arr) {
      const ext = file.name.split(".").pop()?.toLowerCase() ?? "";

      // Block unsupported-on-web formats immediately
      if (WEB_UNSUPPORTED_FORMATS.has(ext)) {
        setShowSizeCTA(true);
        continue;
      }

      // Block oversized files
      const { valid, showDesktopCTA } = checkFileSizeLimit(file);
      if (!valid) {
        setShowSizeCTA(showDesktopCTA);
        continue;
      }

      setQueue((prev) => [
        ...prev,
        { file, sourceExt: ext, targetExt: "", status: "pending" },
      ]);
    }
  }, []);

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files.length) addFiles(e.dataTransfer.files);
  };

  const onDragOver = (e: React.DragEvent) => { e.preventDefault(); setDragActive(true); };
  const onDragLeave = () => setDragActive(false);
  const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) addFiles(e.target.files);
  };

  const updateTarget = (index: number, targetExt: string) => {
    setQueue((prev) => prev.map((item, i) => i === index ? { ...item, targetExt } : item));
  };

  const removeFromQueue = (index: number) => {
    setQueue((prev) => prev.filter((_, i) => i !== index));
  };

  const convertAll = async () => {
    // Only process pending items that have a target format
    const toProcess = queue.map((item, i) => ({ ...item, originalIndex: i }))
                           .filter(item => item.status === "pending" && item.targetExt);
    
    if (toProcess.length === 0) return;

    // Mark as converting
    setQueue(prev => prev.map((item, i) => 
      toProcess.some(p => p.originalIndex === i) 
        ? { ...item, status: "converting", progress: 10 } 
        : item
    ));

    // Process one by one (could be parallel, but one by one is safer for limits)
    for (const item of toProcess) {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setQueue(prev => prev.map((qItem, i) => {
          if (i === item.originalIndex && qItem.status === "converting") {
            return { ...qItem, progress: Math.min((qItem.progress || 10) + 10, 90) };
          }
          return qItem;
        }));
      }, 500);

      const res = await convertFile(item.file, item.sourceExt, item.targetExt);
      
      clearInterval(progressInterval);

      setQueue(prev => prev.map((qItem, i) => {
        if (i === item.originalIndex) {
          if (res.error) {
            return { ...qItem, status: "error", error: res.error };
          }
          return { ...qItem, status: "done", progress: 100, resultUrl: res.resultUrl };
        }
        return qItem;
      }));
    }
  };

  return (
    <div className="flex flex-col gap-md w-full">
      {/* Drop Zone */}
      <div
        className={`drop-zone glass-card flex flex-col items-center justify-center
          min-h-[250px] cursor-pointer p-md select-none
          ${dragActive ? "drag-active" : ""}`}
        onDrop={onDrop}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onClick={() => inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          multiple
          className="hidden"
          onChange={onInputChange}
        />
        <span className="material-symbols-outlined text-primary text-5xl mb-sm">
          upload_file
        </span>
        <p className="text-body-lg text-on-surface font-semibold">
          Drag &amp; Drop files here
        </p>
        <p className="text-label-md text-outline mt-xs">
          or click to browse &mdash; max {WEB_FILE_SIZE_LIMIT_LABEL} per file
        </p>
      </div>

      {/* Desktop CTA (shown on size limit hit or unsupported format) */}
      {showSizeCTA && <DesktopCTA />}

      {/* Queue */}
      {queue.length > 0 && (
        <ConversionQueue
          queue={queue}
          onUpdateTarget={updateTarget}
          onRemove={removeFromQueue}
          onConvertAll={convertAll}
        />
      )}
    </div>
  );
}
