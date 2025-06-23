import requests
from datetime import datetime
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Race(BaseModel):
    race_id: str
    race_time: str
    race_track: str
    race_type: str
    horses: List[Dict]

class RacingAPI:
    def __init__(self):
        self.base_url = os.getenv("RACING_API_BASE_URL")
        self.auth = (
            os.getenv("RACING_API_USERNAME"),
            os.getenv("RACING_API_PASSWORD")
        )
        
    def get_race_cards(self, date: datetime.date) -> List[Race]:
        """Get race cards for a specific date."""
        try:
            # Format date for API
            date_str = date.strftime("%Y-%m-%d")
            
            # Make API request
            url = f"{self.base_url}/racecards/{date_str}"
            response = requests.get(url, auth=self.auth)
            
            # Check response
            response.raise_for_status()
            data = response.json()
            
            # Parse and return races
            return [Race(**race) for race in data.get("races", [])]
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting race cards: {str(e)}")
            return []

    def get_race_details(self, race_id: str) -> Optional[Dict]:
        """Get detailed information about a specific race."""
        try:
            url = f"{self.base_url}/races/{race_id}"
            response = requests.get(url, auth=self.auth)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting race details: {str(e)}")
            return None

    def get_horse_form(self, horse_id: str) -> Optional[Dict]:
        """Get form history for a specific horse."""
        try:
            url = f"{self.base_url}/horses/{horse_id}/form"
            response = requests.get(url, auth=self.auth)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting horse form: {str(e)}")
            return None
