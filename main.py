from fastapi import FastAPI
import requests
from datetime import datetime, timedelta
from twilio.rest import Client
import schedule
import time
import threading
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TO_PHONE_NUMBER = os.getenv("TO_PHONE_NUMBER")

# Garbage Recycling API URL
API_URL = "https://devcorrpublicdatahub.blob.core.usgovcloudapi.net/garbage-recycling/garbagerecyclingdays.json"

def check_recycling():
    try:
        # Fetch data from the API
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        # Define the target recycling zone and calculate tomorrow's date
        target_zone = "Tuesday - B"
        tomorrow = datetime.now() + timedelta(days=1)

        # Find a match for the target zone and date
        target_date_str = None
        for item in data:
            if item.get("Recycling Zone") == target_zone:
                date_str = item.get("Date")
                target_date = datetime.strptime(date_str, "%Y-%m-%d")

                # Check if the target date is tomorrow
                if target_date.date() == tomorrow.date():
                    target_date_str = date_str
                    print(f"Match found: Recycling Zone: {target_zone}, Date: {target_date_str}")
                    break  # Exit loop when a valid match is found

        if not target_date_str:
            print("No match found for the target zone with tomorrow's date.")
            return {"status": "success", "message": "No recycling notification needed for tomorrow."}

        # Send SMS notification
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Reminder: Recycling day for {target_zone} is tomorrow ({target_date_str}).",
            from_=TWILIO_PHONE_NUMBER,
            to=TO_PHONE_NUMBER
        )
        print({"status": "success", "message": "SMS sent", "sid": message.sid})
        return {"status": "success", "message": "SMS sent", "sid": message.sid}

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
