class TrackingService:
    def ingest(self, payload: dict) -> dict:
        return {
            "status": "accepted",
            "payload_keys": sorted(payload.keys()),
        }
