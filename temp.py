import requests
import time

def send_telegram_message():
    # Bot token and user ID
    bot_token = "8087537120:AAHBqn6fu0fOwvUkrAH-2NTxCnvxxm5f1R0"
    user_id = "7448638656"
    message = "привет!"
    
    # Telegram API URL
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # Request payload
    payload = {
        'chat_id': user_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        # Send the request
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        # Check if message was sent successfully
        result = response.json()
        if result.get('ok'):
            print("✅ Message sent successfully!")
            print(f"Message: {message}")
            print(f"User ID: {user_id}")
        else:
            print("❌ Failed to send message")
            print(f"Error: {result.get('description', 'Unknown error')}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    send_telegram_message()
