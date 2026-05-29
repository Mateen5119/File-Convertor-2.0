"use client";

import { CONVERSION_TARGETS } from "@/lib/constants";

type Props = {
  sourceExt: string;
  value: string;
  onChange: (ext: string) => void;
};

export default function FormatSelector({ sourceExt, value, onChange }: Props) {
  const targets = CONVERSION_TARGETS[sourceExt] ?? [];

  if (targets.length === 0) {
    return <span className="text-label-sm text-error">Unsupported on web</span>;
  }

  return (
    <select
      className="sleek-input text-label-md min-w-[80px]"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    >
      <option value="" disabled>to</option>
      {targets.map((t) => (
        <option key={t} value={t}>{t.toUpperCase()}</option>
      ))}
    </select>
  );
}
