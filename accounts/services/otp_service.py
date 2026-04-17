import requests

def send_sms(phone_number: str, message: str) -> bool:
    """
    Connects to AfroMessage to send real SMS to Ethio Telecom/Safaricom.
    """
    url = "https://api.afromessage.com/api/send"
    
    # ⚠️ Replace with your actual AfroMessage credentials
    TOKEN = "YOUR_AFROMESSAGE_TOKEN_HERE" 
    SENDER_ID = "YOUR_SENDER_ID_HERE" 

    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "to": phone_number,
        "from": SENDER_ID,
        "message": message
    }

    try:
        # 10-second timeout so your app doesn't hang
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            res_data = response.json()
            if res_data.get('acknowledge') == 'success' or res_data.get('status') == 'success':
                print(f"✅ SMS sent successfully to {phone_number}")
                return True
        
        # If it fails, we print the error but don't crash the app
        print(f"❌ AfroMessage Error: {response.status_code} - {response.text}")
        return False

    except Exception as e:
        # Fallback print for hackathon testing
        print(f"⚠️ SMS Gateway Connection Failed: {e}")
        print(f"DEBUG ONLY: {message}") 
        return False