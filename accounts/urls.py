import requests

def send_ethio_sms(phone_number, otp_code):
    """
    Sends an OTP via AfroMessage API to Ethiopian phone numbers.
    """
    url = "https://api.afromessage.com/api/send"
    
    # ⚠️ TODO: Replace these with your actual credentials from afromessage.com
    TOKEN = "YOUR_AFROMESSAGE_TOKEN_HERE" 
    SENDER_ID = "YOUR_SENDER_ID_HERE" # Usually "AfroMessage" by default

    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }
    
    payload = {
        "to": phone_number,
        "from": SENDER_ID,
        "message": f"Your Emergency System code is: {otp_code}. Valid for 5 minutes."
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        
        if response.status_code == 200 and response_data.get('acknowledge') == 'success':
            print(f"✅ SMS sent successfully to {phone_number}")
            return True
        else:
            print(f"❌ AfroMessage Error: {response_data}")
            return False
    except Exception as e:
        print(f"⚠️ Connection Error: {e}")
        return False
