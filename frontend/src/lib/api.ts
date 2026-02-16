const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Fixture {
  home_team: string;
  away_team: string;
  match_date: string;
  matchweek: number;
  status: string;
  home_score: number | null;
  away_score: number | null;
}

export interface FixturesResponse {
  week_offset: number;
  week_start: string;
  week_end: string;
  count: number;
  fixtures: Fixture[];
}

export interface MatchPrediction {
  home_team: string;
  away_team: string;
  match_date: string;
  home_win: number;
  draw: number;
  away_win: number;
  home_goals: number;
  away_goals: number;
  home_corners: number;
  away_corners: number;
  home_cards: number;
  away_cards: number;
}

export interface MatchweekResponse {
  predictions: MatchPrediction[];
}

export async function fetchFixtures(weekOffset: number): Promise<FixturesResponse> {
  const res = await fetch(`${API_BASE}/api/fixtures?week_offset=${weekOffset}`);
  if (!res.ok) throw new Error("Failed to fetch fixtures");
  return res.json();
}

export async function predictMatchweek(
  fixtures: { home_team: string; away_team: string; match_date: string }[]
): Promise<MatchweekResponse> {
  const res = await fetch(`${API_BASE}/api/predict/matchweek`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fixtures }),
  });
  if (!res.ok) throw new Error("Failed to predict matchweek");
  return res.json();
}
