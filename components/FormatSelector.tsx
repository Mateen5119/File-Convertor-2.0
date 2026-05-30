"use client";
import { CONVERSION_TARGETS } from "@/lib/constants";

type Props = { sourceExt: string; value: string; onChange: (ext: string) => void };

export default function FormatSelector({ sourceExt, value, onChange }: Props) {
  const targets = CONVERSION_TARGETS[sourceExt.toLowerCase()] ?? [];

  if (targets.length === 0) {
    return (
      <span className="text-label-sm px-2 py-1 rounded-md bg-error-container/20 text-error border border-error/20 whitespace-nowrap">
        Desktop only
      </span>
    );
  }

  return (
    <select
      className="sleek-input text-label-md"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    >
      <option value="" disabled>to…</option>
      {targets.map((t) => (
        <option key={t} value={t}>{t.toUpperCase()}</option>
      ))}
    </select>
  );
}
