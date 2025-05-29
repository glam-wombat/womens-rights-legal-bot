import requests
import json
from typing import Dict, Any, Optional

class RasaConnector:
    """A connector class to interact with the Rasa NLU server."""
    
    def __init__(self, rasa_url: str = "http://localhost:5005"):
        """Initialize the Rasa connector.
        
        Args:
            rasa_url: The URL of the Rasa server.
        """
        self.rasa_url = rasa_url
    
    def parse_message(self, message: str, sender_id: str = "default") -> Dict[str, Any]:
        """Send a message to Rasa for intent and entity extraction.
        
        Args:
            message: The user message to parse.
            sender_id: A unique identifier for the conversation.
            
        Returns:
            A dictionary containing the parsed response from Rasa.
        """
        try:
            # Endpoint for parsing messages
            parse_endpoint = f"{self.rasa_url}/model/parse"
            
            # Prepare the payload
            payload = {
                "text": message
            }
            
            # Send the request to Rasa
            response = requests.post(parse_endpoint, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Parse the response
            parsed_data = response.json()
            return parsed_data
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Rasa server: {e}")
            # Return a default response if Rasa is unavailable
            return {
                "intent": {"name": "nlu_fallback", "confidence": 0.0},
                "entities": [],
                "text": message
            }
    
    def send_message(self, message: str, sender_id: str = "default") -> Optional[Dict[str, Any]]:
        """Send a message to Rasa and get the bot's response.
        
        Args:
            message: The user message to send.
            sender_id: A unique identifier for the conversation.
            
        Returns:
            A dictionary containing the bot's response or None if there was an error.
        """
        try:
            # Endpoint for sending messages
            message_endpoint = f"{self.rasa_url}/webhooks/rest/webhook"
            
            # Prepare the payload
            payload = {
                "sender": sender_id,
                "message": message
            }
            
            # Send the request to Rasa
            response = requests.post(message_endpoint, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Parse the response
            bot_responses = response.json()
            return bot_responses
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Rasa server: {e}")
            return None
    
    def extract_intent_and_entities(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract intent and entities from the parsed data.
        
        Args:
            parsed_data: The parsed data from Rasa.
            
        Returns:
            A dictionary containing the extracted intent and entities.
        """
        intent = parsed_data.get("intent", {}).get("name", "nlu_fallback")
        confidence = parsed_data.get("intent", {}).get("confidence", 0.0)
        entities = parsed_data.get("entities", [])
        
        # Extract entity values
        extracted_entities = {}
        for entity in entities:
            entity_type = entity.get("entity")
            entity_value = entity.get("value")
            if entity_type and entity_value:
                extracted_entities[entity_type] = entity_value
        
        return {
            "intent": intent,
            "confidence": confidence,
            "entities": extracted_entities
        }

# Example usage
if __name__ == "__main__":
    connector = RasaConnector()
    
    # Test parsing a message
    message = "What are my rights under domestic violence law?"
    parsed = connector.parse_message(message)
    extracted = connector.extract_intent_and_entities(parsed)
    
    print(f"Message: {message}")
    print(f"Intent: {extracted['intent']} (confidence: {extracted['confidence']:.2f})")
    print(f"Entities: {extracted['entities']}")
    
    # Test sending a message
    responses = connector.send_message(message)
    if responses:
        for response in responses:
            print(f"Bot: {response.get('text', '')}")