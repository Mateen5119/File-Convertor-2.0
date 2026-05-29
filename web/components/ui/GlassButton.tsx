export default function GlassButton({ children, onClick, className = "" }: { children: React.ReactNode, onClick?: () => void, className?: string }) {
  return (
    <button className={`glass-button-primary ${className}`} onClick={onClick}>
      {children}
    </button>
  );
}
