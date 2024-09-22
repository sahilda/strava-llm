from dotenv import load_dotenv
import requests
import json
import webbrowser
from urllib.parse import urlencode
import os
import copy

# Load environment variables
load_dotenv()

# 1. Strava API Credentials
CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = 'http://localhost'  # Or use the one you've set in Strava app

# 2. Step 1: Redirect to Strava authorization page
auth_url = 'https://www.strava.com/oauth/authorize?' + urlencode({
    'client_id': CLIENT_ID,
    'redirect_uri': REDIRECT_URI,
    'response_type': 'code',
    'scope': 'activity:read_all',  # Scope for reading all activities
    'approval_prompt': 'force'
})

# Open browser for user to authorize the app
print(f"Opening the browser for Strava authorization: {auth_url}")
webbrowser.open(auth_url)

# 3. Step 2: Get the authorization code from the URL
auth_code = input('Paste the authorization code from the URL: ')

# 4. Step 3: Exchange authorization code for an access token
token_url = 'https://www.strava.com/oauth/token'
token_payload = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'code': auth_code,
    'grant_type': 'authorization_code'
}
response = requests.post(token_url, data=token_payload)
token_data = response.json()

# Extract the access token
access_token = token_data['access_token']
print(f"Access token: {access_token}")

# 5. Step 4: Use the access token to make authenticated API requests
# Example: Get recent activities
activities_url = 'https://www.strava.com/api/v3/athlete/activities'
headers = {
    'Authorization': f'Bearer {access_token}'
}
response = requests.get(activities_url, headers=headers)
activities = response.json()

# 6. Filter json
save_keys = ['name', 'distance', 'moving_time', 'elasped_time', 'start_date', 'total_elevation_gain', 'start_date_local',
             'average_speed', 'max_speed', 'average_heartrate', 'max_heartrate', 'elev_high', 'elev_low', 'suffer_score']
data_copy = copy.deepcopy(activities)
for i, d in enumerate(data_copy):
    for k in d.keys():
        if k not in save_keys:
            del activities[i][k]

# 7. Step 5: Save the data to a JSON file
with open('strava_activities.json', 'w') as f:
    json.dump(activities, f, indent=4)

print("Strava activities saved to strava_activities.json")
