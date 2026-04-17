from core.pipeline import run_track2event


class Track2EventService:
    def run(self, params: dict) -> dict:
        result = run_track2event(**params)

        return {
            "track_count": len(result["tracks"]),
            "analyze_count": len(result["analyze_result"]),
            "event_count": len(result["stationary_events"]),
            "stationary_events": result["stationary_events"],
        }