import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings

BASE_URL = "https://api.cricapi.com/v1"


class CricAPIClient:
    def __init__(self):
        self._client = httpx.AsyncClient(timeout=15.0)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=4))
    async def _get(self, endpoint: str, params: dict | None = None) -> dict:
        params = params or {}
        params["apikey"] = settings.CRICAPI_KEY
        resp = await self._client.get(f"{BASE_URL}/{endpoint}", params=params)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "success":
            raise ValueError(f"CricAPI error: {data.get('info', 'unknown')}")
        return data

    # ── Matches ───────────────────────────────────────────────────────────────

    async def list_current_matches(self, offset: int = 0) -> list[dict]:
        data = await self._get("currentMatches", {"offset": offset})
        return data.get("data", [])

    async def list_matches(self, offset: int = 0) -> list[dict]:
        data = await self._get("matches", {"offset": offset})
        return data.get("data", [])

    async def get_match_info(self, match_id: str) -> dict:
        data = await self._get("match_info", {"id": match_id})
        return data.get("data", {})

    async def get_scorecard(self, match_id: str) -> dict:
        data = await self._get("match_scorecard", {"id": match_id})
        return data.get("data", {})

    async def get_live_score(self, match_id: str) -> dict:
        """eCricScore — real-time ball-by-ball live score."""
        data = await self._get("match_scorecard", {"id": match_id})
        return data.get("data", {})

    # ── Series ────────────────────────────────────────────────────────────────

    async def list_series(self, offset: int = 0) -> list[dict]:
        data = await self._get("series", {"offset": offset})
        return data.get("data", [])

    async def get_series_info(self, series_id: str) -> dict:
        data = await self._get("series_info", {"id": series_id})
        return data.get("data", {})

    async def get_series_matches(self, series_id: str) -> list[dict]:
        data = await self._get("series_info", {"id": series_id})
        return data.get("data", {}).get("matchList", [])

    async def get_points_table(self, series_id: str) -> list[dict]:
        data = await self._get("series_points_table", {"id": series_id})
        return data.get("data", [])

    # ── Players ───────────────────────────────────────────────────────────────

    async def search_player(self, name: str) -> list[dict]:
        data = await self._get("players", {"search": name, "offset": 0})
        return data.get("data", [])

    async def get_player_info(self, player_id: str) -> dict:
        data = await self._get("players_info", {"id": player_id})
        return data.get("data", {})

    async def close(self):
        await self._client.aclose()


cricapi = CricAPIClient()
