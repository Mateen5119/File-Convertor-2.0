import { DESKTOP_DOWNLOAD_URL } from "@/lib/constants";

export default function DesktopCTA() {
  return (
    <div className="glass-card rounded-xl p-md flex items-center justify-between gap-md">
      <div className="flex items-center gap-sm">
        <span className="material-symbols-outlined text-primary text-3xl">desktop_mac</span>
        <div>
          <p className="text-headline-md text-on-surface">
            Get File Harbor for Desktop
          </p>
          <p className="text-label-md text-outline">
            No ads, unlimited file sizes, offline processing.
          </p>
        </div>
      </div>
      <a href={DESKTOP_DOWNLOAD_URL} className="glass-button-primary whitespace-nowrap">
        Download Free
        <span className="material-symbols-outlined text-base ml-xs align-middle">
          download
        </span>
      </a>
    </div>
  );
}
