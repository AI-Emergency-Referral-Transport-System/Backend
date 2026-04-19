class AIComprehensiveEmergencyView(APIView):
    """Get comprehensive emergency response with all resources."""
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        user_id = request.data.get('user_id')
        emergency_type = request.data.get('emergency_type', 'other')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        language = request.data.get('language', 'en')
        patient_location = None
        if latitude and longitude:
            patient_location = {'latitude': float(latitude), 'longitude': float(longitude)}
        if not user_id and not patient_location:
            return Response({'error': 'user_id or location coordinates required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = ai_services.get_comprehensive_emergency_response(
                user_id=user_id,
                emergency_type=emergency_type,
                patient_location=patient_location,
                language=language
            )
            if 'error' in result:
                return Response({'success': False, 'error': result.get('error'), 'message': result.get('message')}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True, 'emergency_type': emergency_type, **result})
        except Exception as e:
            logger.error(f"Comprehensive emergency error: {e}")
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class AINearbyResourcesView(APIView):
    """Search nearby ambulances and hospitals."""
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        latitude = request.query_params.get('latitude', type=float)
        longitude = request.query_params.get('longitude', type=float)
        radius = float(request.query_params.get('radius', 30))
        resource_type = request.query_params.get('type', 'both')
        if not latitude or not longitude:
            return Response({'error': 'Latitude and longitude required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = ai_services.search_nearby_resources(latitude, longitude, resource_type, radius)
            return Response({'success': True, 'location': {'latitude': latitude, 'longitude': longitude}, **result})
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class AIAmbulanceListView(APIView):
    """Get available ambulances."""
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        latitude = request.query_params.get('latitude', type=float)
        longitude = request.query_params.get('longitude', type=float)
        radius = float(request.query_params.get('radius', 50))
        emergency_type = request.query_params.get('emergency_type')
        if not latitude or not longitude:
            return Response({'error': 'Latitude and longitude required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if emergency_type:
                ambulances = ambulance_service.get_emergency_ambulances(emergency_type, latitude, longitude)
            else:
                ambulances = ambulance_service.get_available_ambulances(latitude, longitude, radius)
            return Response({'success': True, 'count': len(ambulances), 'ambulances': ambulances})
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class AIHospitalListView(APIView):
    """Get nearby hospitals."""
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        latitude = request.query_params.get('latitude', type=float)
        longitude = request.query_params.get('longitude', type=float)
        radius = float(request.query_params.get('radius', 50))
        emergency_type = request.query_params.get('emergency_type')
        if not latitude or not longitude:
            return Response({'error': 'Latitude and longitude required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if emergency_type:
                hospitals = hospital_service.get_hospitals_by_emergency_type(emergency_type, latitude, longitude)
            else:
                hospitals = hospital_service.get_nearby_hospitals(latitude, longitude, radius)
            return Response({'success': True, 'count': len(hospitals), 'hospitals': hospitals[:10]})
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class AIOneTapCallView(APIView):
    """Get one-tap emergency call info."""
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return Response({
            'success': True,
            'country': 'ethiopia',
            'emergency_number': '907',
            'ambulance': '907',
            'police': '991',
            'fire': '939',
            'instruction': 'One tap to call ambulance dispatch',
            'sms_alternative': 'Send location via SMS to 907'
        })
class AIUserProfileView(APIView):
    """Get user profile for AI context."""
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            from .services import UserProfileService
            user_service = UserProfileService()
            profile = user_service.get_user_profile(user_id)
            if not profile:
                return Response({'success': False, 'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            contacts = user_service.get_emergency_contacts(user_id)
            primary = user_service.get_primary_contact(user_id)
            location = user_service.get_user_location(user_id)
            return Response({'success': True, 'profile': profile, 'emergency_contacts': contacts, 'primary_contact': primary, 'location': location})
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class AIQuickInfoView(APIView):
    """Quick AI info with emergency resources."""
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        message = request.data.get('message', '')
        user_id = request.data.get('user_id')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        language = request.data.get('language', 'en')
        if not message:
            return Response({'error': 'Message required'}, status=status.HTTP_400_BAD_REQUEST)
        patient_location = None
        if latitude and longitude:
            patient_location = {'latitude': float(latitude), 'longitude': float(longitude)}
        message_lower = message.lower()
        result = {'message': message}
        if any(w in message_lower for w in ['hospital', 'ሆስፒታል', 'clinic']):
            if patient_location:
                hospitals = hospital_service.get_nearby_hospitals(patient_location['latitude'], patient_location['longitude'])
                result['hospitals'] = hospitals[:3]
                result['response'] = f"Found {len(hospitals)} nearby hospitals"
            else:
                result['response'] = 'Please provide your location for hospital search'
        elif any(w in message_lower for w in ['ambulance', 'አምቡላንስ']):
            if patient_location:
                ambulances = ambulance_service.get_available_ambulances(patient_location['latitude'], patient_location['longitude'])
                result['ambulances'] = ambulances[:3]
                result['response'] = f"Found {len(ambulances)} available ambulances"
            else:
                result['response'] = 'Please provide your location for ambulance search'
        elif any(w in message_lower for w in ['one tap', 'call 907', 'ይደውሉ']):
            result['response'] = 'Call 907 for ambulance dispatch'
            result['one_tap'] = {'number': '907', 'display': '907', 'instruction': 'One tap to call'}
        else:
            result['response'] = 'I can help find hospitals, ambulances, or emergency contacts. Please specify.'
        return Response(result)
class AIEmergencyDispatchView(APIView):
    """Auto-dispatch with AI and resources."""
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        user_id = request.data.get('user_id')
        emergency_type = request.data.get('emergency_type', 'other')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        description = request.data.get('description', '')
        language = request.data.get('language', 'en')
        if not latitude or not longitude:
            return Response({'error': 'Location required for dispatch'}, status=status.HTTP_400_BAD_REQUEST)
        if not user_id:
            return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = ai_services.get_comprehensive_emergency_response(
                user_id=user_id,
                emergency_type=emergency_type,
                patient_location={'latitude': float(latitude), 'longitude': float(longitude)},
                language=language
            )
            if 'error' in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'success': True,
                'emergency_type': emergency_type,
                'description': description,
                'location': {'latitude': float(latitude), 'longitude': float(longitude), 'maps_link': f"https://maps.google.com/?q={latitude},{longitude}"},
                'dispatch_info': {'ambulance': result.get('nearest_ambulance'), 'hospital': result.get('nearest_hospital'), 'one_tap_call': '907'},
                'all_resources': result
            })
        except Exception as e:
            logger.error(f"Dispatch error: {e}")
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)