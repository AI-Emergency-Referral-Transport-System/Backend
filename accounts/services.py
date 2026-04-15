class OTPService:
    def queue_code(self, phone_number: str) -> dict:
        return {
            "phone_number": phone_number,
            "status": "queued",
        }
