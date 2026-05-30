import { DESKTOP_DOWNLOAD_URL } from "@/lib/constants";

export default function DesktopCTA() {
  return (
    <div className="glass-card rounded-xl p-md flex flex-col sm:flex-row items-start sm:items-center justify-between gap-sm">
      <div className="flex items-start sm:items-center gap-sm">
        <span className="material-symbols-outlined text-primary flex-shrink-0" style={{ fontSize: 36 }}>
          desktop_mac
        </span>
        <div>
          <p className="text-headline-md text-on-surface">Get File Harbor Desktop</p>
          <p className="text-label-md text-outline">
            No ads · Unlimited file sizes · Offline · Editor &amp; compressor
          </p>
        </div>
      </div>
      <a
        href={DESKTOP_DOWNLOAD_URL}
        target="_blank"
        rel="noopener noreferrer"
        className="glass-button-primary flex-shrink-0"
      >
        <span className="material-symbols-outlined" style={{ fontSize: 16 }}>download</span>
        Download Free
      </a>
    </div>
  );
}
