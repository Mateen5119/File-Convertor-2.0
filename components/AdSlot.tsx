type Props = { size: "160x600" | "300x250" };

export default function AdSlot({ size }: Props) {
  const [w, h] = size.split("x").map(Number);
  return (
    <div
      data-ad-slot={size}
      className="glass-card flex flex-col items-center justify-center gap-xs text-outline"
      style={{ width: w, minHeight: h }}
    >
      <span className="material-symbols-outlined opacity-25" style={{ fontSize: 28 }}>campaign</span>
      <span className="text-label-sm opacity-25">Advertisement</span>
    </div>
  );
}
