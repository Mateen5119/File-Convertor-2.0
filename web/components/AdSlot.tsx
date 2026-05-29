type Props = { size: "300x250" | "160x600" };

export default function AdSlot({ size }: Props) {
  const [w, h] = size.split("x").map(Number);
  return (
    <div
      data-ad-slot={size}
      className="glass-card rounded-xl flex items-center justify-center text-outline text-label-sm flex-shrink-0"
      style={{ width: w, height: h }}
    >
      <div className="flex flex-col items-center gap-xs opacity-40">
        <span className="material-symbols-outlined">campaign</span>
        Advertisement
      </div>
    </div>
  );
}
