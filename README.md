# recycling-notification
A simple python app that uses fastAPI, Round Rock's recycling API and Twilio to send a SMS reminder to take out the recycle bin. I made this app because I wanted to test the effectiveness of chatGPT-4o to help me write code as well as explore the use of [FastAPI](https://fastapi.tiangolo.com/) as a framework and solution for Python. 

## How to Configure and Run the App Locally

Follow these steps to set up and run the Python app locally on a Mac:

### 1. Install Prerequisites
Ensure you have the following installed:
- **Python** (version 3.7+)
- **Pip** (Python package manager)

#### Check Python Version:
```bash
python3 --version
```

#### Install Python (if needed):
```bash
brew install python
```

### 2. Clone the Repository
Clone the repository and navigate to the project folder:
```bash
git clone <repository_url>
cd <repository_folder>
```

### 3. Set Up a Virtual Environment
Create a virtual environment to isolate dependencies.

#### Create the Virtual Environment:
```bash
python3 -m venv venv
```
#### Activate the Virtual Environment:
```bash
source venv/bin/activate
```

### 4. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 5. Configure the `.env` File
Create a `.env` file and add the necessary environment variables. This example uses Nano but you could use VIM or your favorite code editor or IDE.

#### Create the `.env` File:
```bash
touch .env
```

#### Edit the `.env` File:
```bash
nano .env
```
Example content:
```plaintext
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
TO_PHONE_NUMBER=+0987654321
```

Save and exit (`Ctrl + O`, `Enter`, `Ctrl + X`).

### 6. Run the App
Start the app using the FastAPI server:
```bash
uvicorn main:app --reload
```
- Replace main with the name of your Python file (without the .py extension).
- Access the app at: `http://127.0.0.1:8000`

### 7. Test the App
Manually trigger the recycling notification or test endpoints.

#### Example: Test Endpoint
```bash
curl http://127.0.0.1:8000/check-recycling
```
- Note: the python code is currently set to check every Monday at 5pm CT. You will need to adjust the `target_zone` and `schedule` (day and time) in order to meet your needs and test the app.

### 8. Deactivate the Virtual Environment
When you're done, deactivate the virtual environment:
```bash
deactivate
```
