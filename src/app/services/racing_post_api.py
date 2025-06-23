import requests
from datetime import datetime
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from ratelimit import limits, sleep_and_retry
import backoff

load_dotenv()

# Racing Post API configuration
RACING_POST_API_BASE = "https://api.racingpost.com"
RACING_POST_API_KEY = os.getenv("RACING_POST_API_KEY")

# Rate limiting: 100 requests per minute
CALLS = 100
PERIOD = 60

class RacingPostAPI:
    def __init__(self):
        self.base_url = RACING_POST_API_BASE
        self.headers = {
            "X-API-Key": RACING_POST_API_KEY,
            "Content-Type": "application/json"
        }
        
    @sleep_and_retry
    @limits(calls=CALLS, period=PERIOD)
    @backoff.on_exception(backoff.expo,
                         (requests.exceptions.RequestException),
                         max_tries=3)
    def get_race_cards(self, date: datetime.date) -> List[Dict]:
        """Get race cards for a specific date."""
        try:
            url = f"{self.base_url}/racecards"
            params = {
                "date": date.isoformat(),
                "include_horses": "true"
            }
            
            response = requests.get(
                url,
                headers=self.headers,
                params=params
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting race cards: {str(e)}")
            raise

    def get_race_details(self, race_id: str) -> Optional[Dict]:
        """Get detailed information about a specific race."""
        try:
            url = f"{self.base_url}/races/{race_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting race details: {str(e)}")
            return None

    def get_horse_form(self, horse_id: str) -> Optional[Dict]:
        """Get form history for a specific horse."""
        try:
            url = f"{self.base_url}/horses/{horse_id}/form"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting horse form: {str(e)}")
            return None
