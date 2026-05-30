"use client";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

export default function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  // Avoid hydration mismatch — render placeholder until mounted
  if (!mounted) return <div style={{ width: 36, height: 36 }} />;

  return (
    <button
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      className="glass-button-primary"
      style={{ padding: "0.375rem 0.5rem" }}
      title="Toggle theme"
      aria-label="Toggle color theme"
    >
      <span className="material-symbols-outlined" style={{ fontSize: 18 }}>
        {theme === "dark" ? "light_mode" : "dark_mode"}
      </span>
    </button>
  );
}
