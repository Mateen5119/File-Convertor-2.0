"use client";

import { useCallback, useRef, useState, useEffect } from "react";
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

  // ISS-010: Ensure Object URLs are revoked on component unmount
  useEffect(() => {
    return () => {
      queue.forEach((item) => {
        if (item.resultUrl) {
          URL.revokeObjectURL(item.resultUrl);
        }
      });
    };
  }, [queue]);

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

      // Block oversized files (>3.3MB)
      const { valid, showDesktopCTA } = checkFileSizeLimit(file);
      if (!valid) {
        setShowSizeCTA(showDesktopCTA);
        continue;
      }

      // ISS-008: Unique UUID to guarantee React index stability
      const id = `${file.name}-${Date.now()}-${Math.random().toString(36).substring(2, 11)}`;

      setQueue((prev) => [
        ...prev,
        { id, file, sourceExt: ext, targetExt: "", status: "pending" },
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

  const updateTarget = (id: string, targetExt: string) => {
    setQueue((prev) => prev.map((item) => item.id === id ? { ...item, targetExt } : item));
  };

  const removeFromQueue = (id: string) => {
    setQueue((prev) => {
      const target = prev.find((item) => item.id === id);
      // ISS-010: Revoke Object URL immediately on removal to prevent memory leak
      if (target?.resultUrl) {
        URL.revokeObjectURL(target.resultUrl);
      }
      return prev.filter((item) => item.id !== id);
    });
  };

  const convertAll = async () => {
    // Only process pending items that have a target format
    const toProcess = queue.filter(item => item.status === "pending" && item.targetExt);
    
    if (toProcess.length === 0) return;

    // Mark selected as converting
    setQueue(prev => prev.map((item) => 
      toProcess.some(p => p.id === item.id) 
        ? { ...item, status: "converting", progress: 10 } 
        : item
    ));

    // Process one by one (could be parallel, but one by one is safer for limits)
    for (const item of toProcess) {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setQueue(prev => prev.map((qItem) => {
          if (qItem.id === item.id && qItem.status === "converting") {
            return { ...qItem, progress: Math.min((qItem.progress || 10) + 10, 90) };
          }
          return qItem;
        }));
      }, 500);

      const res = await convertFile(item.file, item.sourceExt, item.targetExt);
      
      clearInterval(progressInterval);

      setQueue(prev => prev.map((qItem) => {
        if (qItem.id === item.id) {
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
