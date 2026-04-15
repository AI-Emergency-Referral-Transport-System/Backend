class AmbulanceDispatchService:
    def assign_driver(self, ambulance, driver) -> dict:
        return {
            "ambulance_id": str(ambulance.id),
            "driver_id": str(driver.id),
        }
