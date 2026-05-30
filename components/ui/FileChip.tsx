type Status = "pending" | "converting" | "done" | "error";

const STYLES: Record<Status, string> = {
  pending:    "bg-primary/10 text-primary border border-primary/25",
  converting: "bg-secondary/10 text-secondary border border-secondary/25",
  done:       "bg-tertiary/10 text-tertiary border border-tertiary/25",
  error:      "bg-error/10 text-error border border-error/25",
};

export default function FileChip({ ext, status }: { ext: string; status: Status }) {
  return (
    <span className={`text-label-sm px-2 py-0.5 rounded-md uppercase tracking-widest flex-shrink-0 ${STYLES[status]}`}>
      {ext.slice(0, 6)}
    </span>
  );
}
