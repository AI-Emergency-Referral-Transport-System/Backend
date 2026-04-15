class EmergencyLifecycleService:
    transition_map = {
        "requested": {"assigned"},
        "assigned": {"in_progress"},
        "in_progress": {"completed"},
        "completed": set(),
    }

    def transition(self, emergency, next_status: str):
        return {
            "emergency_id": str(emergency.id),
            "next_status": next_status,
        }
