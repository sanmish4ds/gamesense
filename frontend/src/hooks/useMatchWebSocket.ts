import { useEffect, useRef, useCallback } from "react";
import type { LiveMatchEvent } from "../types";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const WS_BASE = API_BASE.replace(/^http/, "ws");

export function useMatchWebSocket(
  matchId: string | undefined,
  onEvent: (event: LiveMatchEvent) => void
) {
  const ws = useRef<WebSocket | null>(null);
  const onEventRef = useRef(onEvent);
  onEventRef.current = onEvent;

  const connect = useCallback(() => {
    if (!matchId) return;
    ws.current = new WebSocket(`${WS_BASE}/ws/matches/${matchId}`);

    ws.current.onmessage = (e) => {
      try {
        const data: LiveMatchEvent = JSON.parse(e.data);
        onEventRef.current(data);
      } catch {
        // ignore malformed frames
      }
    };

    ws.current.onclose = () => {
      // Reconnect after 3s on unexpected close
      setTimeout(connect, 3000);
    };
  }, [matchId]);

  useEffect(() => {
    connect();
    return () => {
      ws.current?.close();
    };
  }, [connect]);
}
