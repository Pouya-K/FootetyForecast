"use client";

import { useState, useEffect, useCallback } from "react";
import { fetchFixtures, predictMatchweek, Fixture, MatchPrediction } from "@/lib/api";
import MatchCard from "@/components/MatchCard";
import WeekNavigation from "@/components/WeekNavigation";

export default function Home() {
  const [weekOffset, setWeekOffset] = useState(0);
  const [fixtures, setFixtures] = useState<Fixture[]>([]);
  const [predictions, setPredictions] = useState<MatchPrediction[]>([]);
  const [weekStart, setWeekStart] = useState("");
  const [weekEnd, setWeekEnd] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadWeek = useCallback(async (offset: number) => {
    setLoading(true);
    setError(null);

    try {
      // Fetch fixtures for the week
      const fixturesData = await fetchFixtures(offset);
      setFixtures(fixturesData.fixtures);
      setWeekStart(fixturesData.week_start);
      setWeekEnd(fixturesData.week_end);

      // If there are fixtures, get predictions
      if (fixturesData.fixtures.length > 0) {
        const matchInputs = fixturesData.fixtures.map((f) => ({
          home_team: f.home_team,
          away_team: f.away_team,
          match_date: f.match_date,
        }));

        const predData = await predictMatchweek(matchInputs);
        setPredictions(predData.predictions);
      } else {
        setPredictions([]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setFixtures([]);
      setPredictions([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadWeek(weekOffset);
  }, [weekOffset, loadWeek]);

  const findPrediction = (fixture: Fixture): MatchPrediction | undefined => {
    return predictions.find(
      (p) =>
        p.home_team === fixture.home_team &&
        p.away_team === fixture.away_team &&
        p.match_date === fixture.match_date
    );
  };

  return (
    <main className="max-w-3xl mx-auto px-4 py-10">
      {/* Header */}
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold tracking-tight text-[var(--text-primary)]">
          FooteyForecast
        </h1>
        <p className="text-sm text-[var(--text-muted)] mt-1">
          Premier League predictions powered by ML
        </p>
      </div>

      {/* Week Navigation */}
      <WeekNavigation
        weekOffset={weekOffset}
        weekStart={weekStart}
        weekEnd={weekEnd}
        onPrev={() => setWeekOffset((o) => o - 1)}
        onNext={() => setWeekOffset((o) => Math.min(o + 1, 0))}
        loading={loading}
      />

      {/* Content */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <div className="w-8 h-8 border-2 border-[var(--accent)] border-t-transparent rounded-full animate-spin" />
          <p className="text-sm text-[var(--text-muted)] mt-4">Loading predictions…</p>
        </div>
      ) : error ? (
        <div className="text-center py-20">
          <p className="text-[var(--red)] text-sm">{error}</p>
          <button
            onClick={() => loadWeek(weekOffset)}
            className="mt-4 text-sm text-[var(--accent)] hover:underline"
          >
            Retry
          </button>
        </div>
      ) : fixtures.length === 0 ? (
        <div className="text-center py-20">
          <p className="text-[var(--text-muted)] text-sm">No fixtures this week.</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {fixtures.map((fixture, i) => (
            <MatchCard key={i} fixture={fixture} prediction={findPrediction(fixture)} />
          ))}
        </div>
      )}
    </main>
  );
}
