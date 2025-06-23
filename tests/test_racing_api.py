from datetime import datetime
from src.app.services.racing_api import RacingAPI

def test_racing_api():
    """Test the Racing API integration."""
    print("\nTesting Racing API...")
    
    # Initialize API client
    api = RacingAPI()
    
    # Get today's date
    today = datetime.now().date()
    
    try:
        # Get race cards
        print(f"\nFetching race cards for {today}")
        race_cards = api.get_race_cards(today)
        
        if race_cards:
            print(f"\nFound {len(race_cards)} race cards")
            
            # Print details about each race
            for i, race in enumerate(race_cards, 1):
                print(f"\nRace {i}:")
                print(f"Track: {race.race_track}")
                print(f"Race Time: {race.race_time}")
                print(f"Race Type: {race.race_type}")
                
                horses = race.horses
                print(f"Number of Horses: {len(horses)}")
                
                # Print details about first horse
                if horses:
                    first_horse = horses[0]
                    print(f"\nFirst Horse:")
                    print(f"Name: {first_horse.get('name')}")
                    print(f"Jockey: {first_horse.get('jockey')}")
                    print(f"Trainer: {first_horse.get('trainer')}")
                    print(f"Odds: {first_horse.get('odds')}")
        else:
            print("No race cards found")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_racing_api()
