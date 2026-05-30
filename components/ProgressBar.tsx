export default function ProgressBar({ value }: { value: number }) {
  return (
    <div className="w-full bg-surface-container rounded-full overflow-hidden mt-1" style={{ height: 5 }}>
      <div
        className="h-full rounded-full transition-all duration-300 ease-out"
        style={{
          width: `${Math.max(0, Math.min(100, value))}%`,
          background: "linear-gradient(90deg, #adc6ff 0%, #4b8eff 100%)",
        }}
      />
    </div>
  );
}
