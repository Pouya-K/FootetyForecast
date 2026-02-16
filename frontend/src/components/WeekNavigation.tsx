"use client";

interface WeekNavigationProps {
  weekOffset: number;
  weekStart: string;
  weekEnd: string;
  onPrev: () => void;
  onNext: () => void;
  loading: boolean;
}

function formatDate(dateStr: string): string {
  return new Date(dateStr + "T12:00:00").toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
  });
}

export default function WeekNavigation({
  weekOffset,
  weekStart,
  weekEnd,
  onPrev,
  onNext,
  loading,
}: WeekNavigationProps) {
  const label =
    weekOffset === 0
      ? "This Week"
      : weekOffset === -1
        ? "Last Week"
        : weekOffset === 1
          ? "Next Week"
          : weekOffset < 0
            ? `${Math.abs(weekOffset)} Weeks Ago`
            : `In ${weekOffset} Weeks`;

  return (
    <div className="flex items-center justify-center gap-6 mb-8">
      <button
        onClick={onPrev}
        disabled={loading}
        className="p-2 rounded-lg border border-[var(--border)] bg-[var(--bg-card)] hover:bg-[var(--bg-card-hover)] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        aria-label="Previous week"
      >
        <svg
          className="w-5 h-5 text-[var(--text-secondary)]"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
      </button>

      <div className="text-center min-w-[200px]">
        <div className="text-lg font-semibold text-[var(--text-primary)]">{label}</div>
        {weekStart && weekEnd && (
          <div className="text-sm text-[var(--text-muted)]">
            {formatDate(weekStart)} – {formatDate(weekEnd)}
          </div>
        )}
      </div>

      <button
        onClick={onNext}
        disabled={loading || weekOffset >= 0}
        className="p-2 rounded-lg border border-[var(--border)] bg-[var(--bg-card)] hover:bg-[var(--bg-card-hover)] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        aria-label="Next week"
      >
        <svg
          className="w-5 h-5 text-[var(--text-secondary)]"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
  );
}
