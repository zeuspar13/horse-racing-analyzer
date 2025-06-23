from typing import Dict, Any, Optional
from pydantic import BaseModel
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from datetime import datetime
import json
from ..models import Race, Horse


class RaceAnalysisRequest(BaseModel):
    race: Dict[str, Any]
    horses: list[Dict[str, Any]]
    odds_data: Optional[Dict[str, Any]] = None
    historical_data: Optional[Dict[str, Any]] = None


class RaceAnalysisResponse(BaseModel):
    winner_prediction: str
    confidence_score: float
    analysis_reasoning: str
    risk_assessment: str
    suggested_stake: float
    expected_profit: float
    odds: float


class ClaudeService:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-sonnet-20240229"

    def format_race_data(self, race: Race, horses: list[Horse]) -> RaceAnalysisRequest:
        """Format race data for Claude analysis."""
        race_data = {
            "date": race.race_date.isoformat(),
            "track": race.track,
            "distance": race.distance,
            "race_type": race.race_type,
            "class_rating": race.class_rating,
            "total_runners": race.total_runners
        }

        horses_data = []
        for horse in horses:
            horse_data = {
                "name": horse.name,
                "jockey": horse.jockey,
                "trainer": horse.trainer,
                "odds": horse.odds,
                "starting_position": horse.starting_position,
                "weight": horse.weight,
                "last_race_days": horse.last_race_days,
                "wins": horse.wins,
                "places": horse.places,
                "starts": horse.starts,
                "avg_position": horse.avg_position
            }
            horses_data.append(horse_data)

        return RaceAnalysisRequest(
            race=race_data,
            horses=horses_data
        )

    def analyze_race(self, race: Race, horses: list[Horse]) -> RaceAnalysisResponse:
        """Analyze a race using Claude."""
        request = self.format_race_data(race, horses)
        
        prompt = f"{HUMAN_PROMPT}"
        prompt += "You are a professional horse racing analyst. Please analyze the following race and provide a detailed prediction."
        prompt += "\n\nRace Details:\n"
        prompt += json.dumps(request.race, indent=2)
        prompt += "\n\nHorses:\n"
        prompt += json.dumps(request.horses, indent=2)
        
        # Add analysis instructions
        prompt += "\n\nPlease provide your analysis in the following JSON format:\n"
        prompt += "{\n    \"winner\": \"HorseName\",\n    \"confidence\": 85.0,\n    \"reasoning\": \"Detailed reasoning for your prediction\",\n    \"risk\": \"Risk assessment (LOW, MEDIUM, HIGH)\",\n    \"stake\": 0.05,\n    \"profit\": 3.5,\n    \"odds\": 3.5\n}\n"
        
        prompt += "\nMake sure to return ONLY the JSON object. Do not include any additional text."
        prompt += f"\n{AI_PROMPT}"

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Get Claude's response
            content = response.content
            print(f"\nClaude's Raw Response: {content}")
            
            # Try to extract JSON from the response
            try:
                # First try to extract JSON if it's in the response
                import re
                json_match = re.search(r'\{.*?\}', content)
                if json_match:
                    json_str = json_match.group(0)
                    response_data = json.loads(json_str)
                    
                    # Validate the response data
                    winner = response_data.get("winner")
                    if not winner:
                        raise ValueError("No winner predicted in response")
                    
                    return RaceAnalysisResponse(
                        winner_prediction=winner,
                        confidence_score=response_data.get("confidence", 75.0),
                        analysis_reasoning=response_data.get("reasoning", "No reasoning provided"),
                        risk_assessment=response_data.get("risk", "Unknown"),
                        suggested_stake=response_data.get("stake", 0.05),
                        expected_profit=response_data.get("profit", 0.0),
                        odds=response_data.get("odds", 0.0)
                    )
                
            except (json.JSONDecodeError, ValueError):
                # If we can't extract JSON, try to parse the response as text
                print("\nCould not extract JSON from Claude's response")
                
                # Look for winner prediction in the text
                winner = "Unknown"
                confidence = 50.0
                reasoning = "Could not parse Claude's response"
                
                # Look for specific patterns in the text
                if "winner" in content.lower():
                    # Try to find the predicted winner
                    winner_match = re.search(r'winner.*?:\s*(\w+)', content, re.IGNORECASE)
                    if winner_match:
                        winner = winner_match.group(1)
                        confidence = 75.0
                        reasoning = f"Extracted winner prediction: {winner}"
                
                return RaceAnalysisResponse(
                    winner_prediction=winner,
                    confidence_score=confidence,
                    analysis_reasoning=reasoning,
                    risk_assessment="Unknown",
                    suggested_stake=0.05,
                    expected_profit=0.0,
                    odds=0.0
                )
            except Exception as e:
                print(f"\nError processing Claude response: {str(e)}")
                return RaceAnalysisResponse(
                    winner_prediction="Unknown",
                    confidence_score=50.0,
                    analysis_reasoning=f"Error: {str(e)}",
                    risk_assessment="Unknown",
                    suggested_stake=0.05,
                    expected_profit=0.0,
                    odds=0.0
                )
                print(f"\nError processing Claude response: {str(e)}")
                return RaceAnalysisResponse(
                    winner_prediction="Unknown",
                    confidence_score=50.0,
                    analysis_reasoning=f"Error: {str(e)}",
                    risk_assessment="Unknown",
                    suggested_stake=0.05,
                    expected_profit=0.0,
                    odds=0.0
                )
            
        except Exception as e:
            raise Exception(f"Claude analysis failed: {str(e)}")
