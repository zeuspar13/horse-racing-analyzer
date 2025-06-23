from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from ..models import Race, Horse


class RacingPostService:
    def __init__(self):
        self.base_url = "https://www.racingpost.com"
        
    def get_race_cards(self, date: datetime.date) -> List[Dict]:
        """Get race cards for a specific date from Racing Post."""
        url = f"{self.base_url}/racecards"
        print(f"\nStarting to fetch race cards from {url} for date: {date}")
        
        # Configure Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        try:
            # Start the browser
            print("Starting Chrome browser...")
            driver = webdriver.Chrome(options=chrome_options)
            
            # Navigate to page
            print("Navigating to Racing Post...")
            driver.get(url)
            
            # Wait for the race cards to load
            print("Waiting for race cards to load...")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "rp-racecard__race-card"))
            )
            
            # Get the page content
            print("Getting page content...")
            page_content = driver.page_source
            soup = BeautifulSoup(page_content, 'html.parser')
            
            # Find all race cards
            print("Finding race cards...")
            race_cards = []
            race_card_elements = soup.find_all("div", class_="rp-racecard__race-card")
            print(f"Found {len(race_card_elements)} race cards")
            
            # Process each race card
            for i, race_card in enumerate(race_card_elements, 1):
                print(f"\nProcessing race card {i}/{len(race_card_elements)}...")
                race_data = self._parse_race_card(race_card)
                if race_data:
                    race_cards.append(race_data)
                    print(f"Successfully parsed race at {race_data['race_track']}")
                else:
                    print(f"Failed to parse race card {i}")
            
            print(f"\nFinished processing {len(race_cards)} race cards")
            return race_cards
            
        except Exception as e:
            print(f"\nError getting race cards: {str(e)}")
            return []
        finally:
            print("Closing browser...")
            driver.quit()

    def _parse_race_card(self, race_card: BeautifulSoup) -> Optional[Dict]:
        """Parse a single race card element."""
        try:
            # Get race details
            race_time = race_card.find("div", class_="rp-racecard__race-time").text.strip()
            race_track = race_card.find("div", class_="rp-racecard__race-track").text.strip()
            
            # Get race type and distance
            race_info = race_card.find("div", class_="rp-racecard__race-info").text.strip()
            race_type = race_info.split(" ")[0]
            
            # Get horses
            horses = []
            horse_elements = race_card.find_all("div", class_="rp-racecard__horse")
            for horse in horse_elements:
                horse_data = self._parse_horse(horse)
                if horse_data:
                    horses.append(horse_data)
            
            return {
                "race_time": race_time,
                "race_track": race_track,
                "race_type": race_type,
                "horses": horses
            }
            
        except Exception as e:
            print(f"Error parsing race card: {str(e)}")
            return None

    def _parse_horse(self, horse_element: BeautifulSoup) -> Optional[Dict]:
        """Parse a single horse element."""
        try:
            horse_name = horse_element.find("div", class_="rp-racecard__horse-name").text.strip()
            jockey = horse_element.find("div", class_="rp-racecard__jockey").text.strip()
            trainer = horse_element.find("div", class_="rp-racecard__trainer").text.strip()
            odds = horse_element.find("div", class_="rp-racecard__odds").text.strip()
            
            return {
                "name": horse_name,
                "jockey": jockey,
                "trainer": trainer,
                "odds": float(odds) if odds else None
            }
            
        except Exception as e:
            print(f"Error parsing horse: {str(e)}")
            return None

    def save_race_cards_to_db(self, db, date: datetime.date):
        """Save race cards to database."""
        race_cards = self.get_race_cards(date)
        
        for race_card in race_cards:
            # Create race
            race = Race(
                race_date=date,
                track=race_card["race_track"],
                race_type=race_card["race_type"],
                created_at=datetime.utcnow()
            )
            db.add(race)
            db.flush()  # Get the race ID
            
            # Create horses
            for horse_data in race_card["horses"]:
                horse = Horse(
                    race_id=race.id,
                    name=horse_data["name"],
                    jockey=horse_data["jockey"],
                    trainer=horse_data["trainer"],
                    odds=horse_data["odds"],
                    created_at=datetime.utcnow()
                )
                db.add(horse)
            
        db.commit()
