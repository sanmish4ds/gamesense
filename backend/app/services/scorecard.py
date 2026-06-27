from app.models.match import Match


def compute_run_rate(runs: int, overs: float) -> float:
    if overs <= 0:
        return 0.0
    return round(runs / overs, 2)


def required_run_rate(target: int, remaining_runs: int, remaining_overs: float) -> float:
    if remaining_overs <= 0:
        return 0.0
    return round(remaining_runs / remaining_overs, 2)


def build_live_scorecard(match: Match) -> dict:
    """Build a structured scorecard dict from a Match ORM object."""
    scores = []
    if match.score:
        for s in match.score:
            overs = float(s.get("o", 0))
            runs = int(s.get("r", 0))
            scores.append({
                "inning": s.get("inning", ""),
                "runs": runs,
                "wickets": int(s.get("w", 0)),
                "overs": overs,
                "run_rate": compute_run_rate(runs, overs),
            })

    return {
        "match_id": match.id,
        "name": match.name,
        "status": match.status,
        "venue": match.venue,
        "match_type": match.match_type,
        "is_live": match.is_live,
        "teams": {
            "team1": match.team1_name,
            "team2": match.team2_name,
        },
        "batting_team": match.batting_team,
        "bowling_team": match.bowling_team,
        "current_over": match.current_over,
        "scores": scores,
        "toss": match.toss,
        "match_winner": match.match_winner,
        "full_scorecard": match.scorecard,
    }
