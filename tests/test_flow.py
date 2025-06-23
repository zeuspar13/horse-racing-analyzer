import requests
import json
from datetime import datetime
import time

def test_race_analysis_flow():
    # Base URL for our API
    BASE_URL = "http://localhost:8000"
    
    print("\nStarting test flow demonstration...")
    
    # 1. Create a Race
    print("\n1. Creating a race...")
    race_data = {
        "race_date": datetime.now().isoformat(),
        "track": "Ayr",
        "distance": 1600,
        "race_type": "Flat",
        "class_rating": 7
    }
    race_response = requests.post(f"{BASE_URL}/races", json=race_data)
    assert race_response.status_code == 201
    race = race_response.json()
    print(f"Created race with ID: {race['id']}")
    
    # 2. Add Horses
    print("\n2. Adding horses...")
    horses = [
        {
            "race_id": race['id'],
            "name": "Golden Eagle",
            "jockey": "John Smith",
            "trainer": "Bob Brown",
            "odds": 3.5
        },
        {
            "race_id": race['id'],
            "name": "Silver Streak",
            "jockey": "Mike Johnson",
            "trainer": "Sarah Green",
            "odds": 2.5
        },
        {
            "race_id": race['id'],
            "name": "Bronze Bolt",
            "jockey": "Tom Wilson",
            "trainer": "David White",
            "odds": 4.0
        }
    ]
    
    for horse in horses:
        horse_response = requests.post(f"{BASE_URL}/horses", json=horse)
        assert horse_response.status_code == 201
        print(f"Added horse: {horse['name']}")
    
    # 3. Analyze Race
    print("\n3. Analyzing race...")
    analysis_response = requests.post(f"{BASE_URL}/analyze/{race['id']}")
    assert analysis_response.status_code == 201
    analysis = analysis_response.json()
    
    # Print Claude's complete analysis
    print("\nClaude's Analysis Details:")
    print(f"Winner Prediction: {analysis['winner_prediction']}")
    print(f"Confidence Score: {analysis['confidence_score']}%")
    print(f"Analysis Reasoning: {analysis['analysis_reasoning']}")
    print(f"Risk Assessment: {analysis['risk_assessment']}")
    print(f"Suggested Stake: ${analysis['stake_recommendation']}")
    print(f"Expected Profit: ${analysis['expected_profit']}")
    print(f"Odds: {analysis['odds']}")
    
    # Print the raw Claude response
    print("\nRaw Claude Response:")
    print(analysis_response.text)
    
    # 4. Place Bet
    print("\n4. Placing bet...")
    bet_data = {
        "race_id": race['id'],
        "horse_id": 1,  # First horse ID
        "stake": analysis['stake_recommendation'],
        "odds": analysis['odds'],
        "bet_type": "WIN"
    }
    bet_response = requests.post(f"{BASE_URL}/bets", json=bet_data)
    assert bet_response.status_code == 201
    bet = bet_response.json()
    print(f"Bet placed with stake: ${bet['stake']}")
    
    # 5. Update Bet Result
    print("\n5. Updating bet result...")
    update_data = {
        "result": "WON",
        "profit": analysis['expected_profit']
    }
    update_response = requests.put(f"{BASE_URL}/bets/{bet['id']}", json=update_data)
    assert update_response.status_code == 200
    print("Bet result updated successfully")
    
    # 6. Check Bankroll
    print("\n6. Checking bankroll...")
    bankroll_response = requests.get(f"{BASE_URL}/bankroll/1")
    assert bankroll_response.status_code == 200
    bankroll = bankroll_response.json()
    print(f"Current bankroll: ${bankroll['current_amount']}")
    
    print("\nTest flow completed successfully!")

if __name__ == "__main__":
    test_race_analysis_flow()
