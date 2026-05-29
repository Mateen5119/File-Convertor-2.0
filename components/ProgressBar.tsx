type Props = { value: number }; // 0–100

export default function ProgressBar({ value }: Props) {
  return (
    <div className="w-full bg-surface-container rounded-full h-1.5 mt-xs overflow-hidden">
      <div
        className="bg-primary h-full rounded-full transition-all duration-300 ease-linear"
        style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
      />
    </div>
  );
}
