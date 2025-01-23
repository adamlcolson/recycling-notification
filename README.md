# recycling-notification
Simple fastAPI python app that uses Round Rock's recycling API and Twilio to send a SMS reminder to take out the recycle bin.

To make this work with Twilio, add a .env file in the root project folder with the following configs from your Twilio account

```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
TO_PHONE_NUMBER=phone_number_to_send_sms_to
```
