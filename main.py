from fastapi import FastAPI
import requests
from datetime import datetime, timedelta
from twilio.rest import Client
import schedule
import time
import threading

app = FastAPI()

# Twilio configuration
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_phone_number"
TO_PHONE_NUMBER = "recipient_phone_number"

# Garbage Recycling API URL
API_URL = "https://devcorrpublicdatahub.blob.core.usgovcloudapi.net/garbage-recycling/garbagerecyclingdays.json"

def check_recycling():
    try:
        # Fetch data from the API
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        # Find the date for "Recycling Zone": "Tuesday - B"
        target_zone = "Tuesday - B"
        target_date_str = None
        for item in data:
            if item.get("Recycling Zone") == target_zone:
                target_date_str = item.get("Date")
                break

        if not target_date_str:
            return {"status": "error", "message": "Zone not found in data"}

        # Parse the date from the API
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d")

        # Check if the target date is tomorrow
        tomorrow = datetime.now() + timedelta(days=1)
        if target_date.date() == tomorrow.date():
            # Send SMS notification
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"Reminder: Recycling day for {target_zone} is tomorrow ({target_date_str}).",
                from_=TWILIO_PHONE_NUMBER,
                to=TO_PHONE_NUMBER
            )
            print({"status": "success", "message": "SMS sent", "sid": message.sid})
            return {"status": "success", "message": "SMS sent", "sid": message.sid}

        print({"status": "success", "message": "No recycling notification needed for tomorrow."})
        return {"status": "success", "message": "No recycling notification needed for tomorrow."}

    except requests.exceptions.RequestException as e:
        print({"status": "error", "message": f"API request failed: {str(e)}"})
        return {"status": "error", "message": f"API request failed: {str(e)}"}
    except Exception as e:
        print({"status": "error", "message": f"An error occurred: {str(e)}"})
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

# Schedule the task to run every Monday at 5 PM Central Time
def schedule_task():
    schedule.every().monday.at("17:00").do(check_recycling)

    while True:
        schedule.run_pending()
        time.sleep(1)

# Run the scheduler in a separate thread to avoid blocking the FastAPI server
thread = threading.Thread(target=schedule_task)
thread.daemon = True
thread.start()

@app.get("/check-recycling")
def manual_check():
    return check_recycling()
