class HospitalSelectionService:
    def shortlist(self, emergency_location, limit: int = 5) -> dict:
        return {
            "limit": limit,
            "status": "pending_selection_logic",
        }
