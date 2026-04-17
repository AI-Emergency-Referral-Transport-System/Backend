from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Ambulance

class AmbulanceDispatchService:
   

    @transaction.atomic
    def accept_emergency(self, driver_user, emergency_request) -> dict:
        
        try:
            ambulance = Ambulance.objects.select_for_update().get(driver=driver_user)
        except Ambulance.DoesNotExist:
            raise ValidationError("User is not assigned to an active ambulance.")

        if ambulance.status != Ambulance.Status.AVAILABLE:
            raise ValidationError(f"Ambulance is currently {ambulance.status}.")


        ambulance.status = Ambulance.Status.DISPATCHED
        ambulance.save()

        emergency_request.status = "dispatched"
        emergency_request.ambulance = ambulance
        emergency_request.dispatched_at = timezone.now()
        emergency_request.save()

        return {
            "ambulance_id": str(ambulance.id),
            "plate_number": ambulance.plate_number,
            "emergency_id": str(emergency_request.id),
            "status": "success",
            "message": "Dispatch confirmed. Proceed to pickup location."
        }

    @transaction.atomic
    def update_location(self, ambulance_id, latitude, longitude):
        
        ambulance = Ambulance.objects.get(id=ambulance_id)
        ambulance.latitude = latitude
        ambulance.longitude = longitude
        ambulance.last_location_update = timezone.now()
        ambulance.save()
        
        return True