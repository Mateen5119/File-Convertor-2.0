export interface ConvertResult {
  resultUrl?: string;
  error?: string;
}

export async function convertFile(
  file: File,
  sourceExt: string,
  targetExt: string
): Promise<ConvertResult> {
  try {
    // Fast asynchronous base64 encoding using FileReader
    const b64 = await new Promise<string>((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const result = reader.result as string;
        // The result is a data URL like "data:image/png;base64,..."
        // We only want the base64 payload.
        resolve(result.substring(result.indexOf(',') + 1));
      };
      reader.onerror = () => reject(new Error("File read failed"));
      reader.readAsDataURL(file);
    });

    const res = await fetch("/api/convert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        file: b64,
        source_fmt: sourceExt,
        target_fmt: targetExt,
      }),
    });

    // Check if the response is valid JSON
    let data;
    try {
      data = await res.json();
    } catch {
      return { error: "Network error or unexpected response from the server." };
    }

    if (!res.ok || data.error) {
      return { error: data.message || "Conversion failed. Please try the desktop app." };
    }

    const mimeTypes: Record<string, string> = {
      jpg:   "image/jpeg",
      jpeg:  "image/jpeg",
      png:   "image/png",
      webp:  "image/webp",
      tiff:  "image/tiff",
      pdf:   "application/pdf",
      docx:  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      xlsx:  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      csv:   "text/csv",
      json:  "application/json",
      html:  "text/html",
      woff2: "font/woff2",
      crt:   "application/x-x509-ca-cert",
      pfx:   "application/x-pkcs12",
    };

    const mime = mimeTypes[data.target_fmt] ?? "application/octet-stream";
    
    // Fast native decoding using fetch data URL
    const fetchRes = await fetch(`data:${mime};base64,${data.result}`);
    const blob = await fetchRes.blob();
    
    return { resultUrl: URL.createObjectURL(blob) };
  } catch {
    return { error: "Network error. Check your connection and try again." };
  }
}
