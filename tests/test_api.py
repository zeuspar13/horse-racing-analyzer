import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Get API credentials
username = os.getenv("RACING_API_USERNAME")
password = os.getenv("RACING_API_PASSWORD")
base_url = os.getenv("RACING_API_BASE_URL")

print("\nTesting Racing API...")

# Get today's date
now = datetime.now()
today = now.strftime("%Y-%m-%d")

# Test getting race cards
print(f"\nFetching race cards for {today}...")
url = f"{base_url}/v1/racecards/{today}"  # Updated endpoint with version

try:
    response = requests.get(url, auth=(username, password))
    print(f"\nResponse status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\nResponse data:")
        print(json.dumps(data, indent=2))  # Pretty print JSON
        
        print(f"\nFound {len(data.get('races', []))} races")
        print("\nFirst race details:")
        if data.get('races'):
            first_race = data['races'][0]
            print(f"Track: {first_race.get('track')}")
            print(f"Race Time: {first_race.get('time')}")
            print(f"Race Type: {first_race.get('type')}")
            
            # Print horse details
            if first_race.get('horses'):
                print("\nFirst horse details:")
                first_horse = first_race['horses'][0]
                print(f"Name: {first_horse.get('name')}")
                print(f"Jockey: {first_horse.get('jockey')}")
                print(f"Trainer: {first_horse.get('trainer')}")
                print(f"Odds: {first_horse.get('odds')}")
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    print("\nDetailed error:")
    print(traceback.format_exc())
