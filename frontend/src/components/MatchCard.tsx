"use client";

import { Fixture, MatchPrediction } from "@/lib/api";

interface MatchCardProps {
  fixture: Fixture;
  prediction?: MatchPrediction;
}

function StatRow({ label, home, away }: { label: string; home: string; away: string }) {
  return (
    <div className="flex items-center justify-between text-sm py-1">
      <span className="w-16 text-right font-medium text-[var(--text-primary)]">{home}</span>
      <span className="text-xs text-[var(--text-muted)] uppercase tracking-wider w-20 text-center">
        {label}
      </span>
      <span className="w-16 text-left font-medium text-[var(--text-primary)]">{away}</span>
    </div>
  );
}

function ProbabilityBar({
  homeWin,
  draw,
  awayWin,
}: {
  homeWin: number;
  draw: number;
  awayWin: number;
}) {
  const hPct = Math.round(homeWin);
  const dPct = Math.round(draw);
  const aPct = 100 - hPct - dPct;

  return (
    <div className="mt-3 mb-1">
      <div className="flex justify-between text-xs mb-1.5">
        <span className="text-[var(--green)] font-semibold">{hPct}%</span>
        <span className="text-[var(--text-muted)] font-semibold">{dPct}%</span>
        <span className="text-[var(--accent)] font-semibold">{aPct}%</span>
      </div>
      <div className="flex h-2 rounded-full overflow-hidden gap-0.5">
        <div
          className="rounded-l-full transition-all duration-500"
          style={{ width: `${hPct}%`, backgroundColor: "var(--green)" }}
        />
        <div
          className="transition-all duration-500"
          style={{ width: `${dPct}%`, backgroundColor: "var(--text-muted)" }}
        />
        <div
          className="rounded-r-full transition-all duration-500"
          style={{ width: `${aPct}%`, backgroundColor: "var(--accent)" }}
        />
      </div>
      <div className="flex justify-between text-[10px] mt-1 text-[var(--text-muted)]">
        <span>Home</span>
        <span>Draw</span>
        <span>Away</span>
      </div>
    </div>
  );
}

function isPastMatch(fixture: Fixture): boolean {
  return fixture.status === "FINISHED";
}

export default function MatchCard({ fixture, prediction }: MatchCardProps) {
  const finished = isPastMatch(fixture);

  return (
    <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5 hover:bg-[var(--bg-card-hover)] transition-colors duration-200">
      {/* Match Date */}
      <div className="text-center text-xs text-[var(--text-muted)] mb-3 uppercase tracking-wider">
        {new Date(fixture.match_date + "T12:00:00").toLocaleDateString("en-GB", {
          weekday: "short",
          day: "numeric",
          month: "short",
        })}
        {fixture.matchweek && (
          <span className="ml-2 text-[var(--text-muted)]">• GW{fixture.matchweek}</span>
        )}
      </div>

      {/* Real Result (for past matches) */}
      {finished && fixture.home_score !== null && fixture.away_score !== null && (
        <div className="mb-4">
          <div className="text-center text-[10px] uppercase tracking-widest text-[var(--text-muted)] mb-2">
            Full Time
          </div>
          <div className="flex items-center justify-between">
            <span className="text-base font-semibold text-[var(--text-primary)] flex-1 text-right">
              {fixture.home_team}
            </span>
            <div className="mx-4 flex items-center gap-2">
              <span className="text-2xl font-bold text-[var(--text-primary)]">
                {fixture.home_score}
              </span>
              <span className="text-lg text-[var(--text-muted)]">-</span>
              <span className="text-2xl font-bold text-[var(--text-primary)]">
                {fixture.away_score}
              </span>
            </div>
            <span className="text-base font-semibold text-[var(--text-primary)] flex-1 text-left">
              {fixture.away_team}
            </span>
          </div>
          <div className="border-b border-[var(--border)] mt-4 mb-3" />
        </div>
      )}

      {/* Prediction Section */}
      {prediction ? (
        <div>
          {finished && (
            <div className="text-center text-[10px] uppercase tracking-widest text-[var(--accent)] mb-2">
              Prediction
            </div>
          )}

          {/* Team Names (only show if not finished, since finished already shows them) */}
          {!finished && (
            <div className="flex items-center justify-between mb-1">
              <span className="text-base font-semibold text-[var(--text-primary)] flex-1 text-right">
                {fixture.home_team}
              </span>
              <span className="text-xs text-[var(--text-muted)] mx-3">vs</span>
              <span className="text-base font-semibold text-[var(--text-primary)] flex-1 text-left">
                {fixture.away_team}
              </span>
            </div>
          )}

          {/* Win Probability */}
          <ProbabilityBar
            homeWin={prediction.home_win}
            draw={prediction.draw}
            awayWin={prediction.away_win}
          />

          {/* Detailed Stats */}
          <div className="mt-3 pt-3 border-t border-[var(--border)] space-y-0.5">
            <StatRow
              label="Goals"
              home={prediction.home_goals.toFixed(1)}
              away={prediction.away_goals.toFixed(1)}
            />
            <StatRow
              label="Corners"
              home={prediction.home_corners.toFixed(1)}
              away={prediction.away_corners.toFixed(1)}
            />
            <StatRow
              label="Cards"
              home={prediction.home_cards.toFixed(1)}
              away={prediction.away_cards.toFixed(1)}
            />
          </div>
        </div>
      ) : (
        /* No prediction yet - just show teams */
        <div className="flex items-center justify-between">
          <span className="text-base font-semibold text-[var(--text-primary)] flex-1 text-right">
            {fixture.home_team}
          </span>
          <span className="text-xs text-[var(--text-muted)] mx-3">vs</span>
          <span className="text-base font-semibold text-[var(--text-primary)] flex-1 text-left">
            {fixture.away_team}
          </span>
        </div>
      )}
    </div>
  );
}
