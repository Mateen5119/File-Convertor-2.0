type Status = "pending" | "converting" | "done" | "error";

const COLOR: Record<Status, string> = {
  pending:    "bg-primary/10 text-primary border border-primary/30",
  converting: "bg-secondary-container/20 text-secondary border border-secondary/30",
  done:       "bg-tertiary-container/20 text-tertiary border border-tertiary/30",
  error:      "bg-error-container/30 text-error border border-red-500/30",
};

type Props = { ext: string; status: Status };

export default function FileChip({ ext, status }: Props) {
  return (
    <span className={`text-label-sm px-2 py-0.5 rounded-md uppercase tracking-widest flex-shrink-0 ${COLOR[status]}`}>
      {ext}
    </span>
  );
}
