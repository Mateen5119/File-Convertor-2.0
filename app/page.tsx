import DropZone from "@/components/DropZone";
import AdSlot from "@/components/AdSlot";
import DesktopCTA from "@/components/DesktopCTA";
import ThemeToggle from "@/components/ThemeToggle";

export default function Home() {
  return (
    <>
      {/* Ambient blobs (behind everything) */}
      <div className="ambient-blob blob-1" />
      <div className="ambient-blob blob-2" />

      {/* Nav */}
      <header className="glass-pane sticky top-0 z-10 px-margin py-sm flex items-center justify-between">
        <span className="text-headline-md text-on-surface font-bold">File Harbor</span>
        <nav className="flex gap-md text-label-md text-outline items-center">
          <a href="#" className="hover:text-on-surface transition-colors">Tools</a>
          <a href="#" className="hover:text-on-surface transition-colors">Pricing</a>
          <a href="#" className="hover:text-on-surface transition-colors">Help</a>
          <ThemeToggle />
        </nav>
        <button className="glass-button-primary hidden sm:block">Sign In</button>
      </header>

      {/* Hero */}
      <main className="max-w-app mx-auto px-gutter py-lg min-h-[calc(100vh-160px)]">
        <div className="text-center mb-lg">
          <h1 className="text-display text-on-surface mb-sm">
            Effortless File Conversion.
          </h1>
          <p className="text-body-lg text-outline max-w-xl mx-auto">
            Transform your documents, images, and media instantly.
            Drag, drop, and done — with uncompromising precision.
          </p>
        </div>

        {/* Three-column layout: ad | workspace | ad */}
        <div className="flex items-start gap-gutter justify-center">
          {/* Left ad (hidden on mobile) */}
          <div className="hidden lg:block flex-shrink-0">
            <AdSlot size="160x600" />
          </div>

          {/* Center workspace */}
          <div className="flex-grow max-w-2xl flex flex-col gap-md">
            <DropZone />
            <DesktopCTA />
          </div>

          {/* Right ad (hidden on mobile) */}
          <div className="hidden lg:block flex-shrink-0">
            <AdSlot size="160x600" />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="glass-pane mt-lg px-margin py-md flex flex-col sm:flex-row gap-4 items-center justify-between text-label-sm text-outline">
        <span>© 2026 File Harbor. Precision Processing.</span>
        <div className="flex gap-md">
          <a href="#" className="hover:text-on-surface transition-colors">Privacy Policy</a>
          <a href="#" className="hover:text-on-surface transition-colors">Terms of Service</a>
          <a href="#" className="hover:text-on-surface transition-colors">Contact</a>
        </div>
      </footer>
    </>
  );
}
