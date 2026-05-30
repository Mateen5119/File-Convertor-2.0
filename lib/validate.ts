import { WEB_FILE_SIZE_LIMIT_BYTES } from "./constants";

export interface FileSizeCheck {
  valid: boolean;
  showDesktopCTA: boolean;
  reason?: string;
}

export function checkFileSizeLimit(file: File): FileSizeCheck {
  if (file.size > WEB_FILE_SIZE_LIMIT_BYTES) {
    return {
      valid: false,
      showDesktopCTA: true,
      reason: `${(file.size / 1_000_000).toFixed(1)}MB exceeds the 3.3MB web limit.`,
    };
  }
  return { valid: true, showDesktopCTA: false };
}
