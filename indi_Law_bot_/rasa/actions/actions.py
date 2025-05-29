from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json
import os
import requests
from googletrans import Translator

# Initialize translator
translator = Translator()

# Load the knowledge base
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
with open(os.path.join(data_dir, "laws.json"), "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# Helper functions
def translate_text(text: str, target_language: str) -> str:
    """Translate text to the target language."""
    if target_language.lower() == "english":
        return text
    
    try:
        # Map language names to language codes
        language_codes = {
            "hindi": "hi",
            "bengali": "bn",
            "telugu": "te",
            "marathi": "mr",
            "tamil": "ta",
            "urdu": "ur",
            "gujarati": "gu",
            "kannada": "kn",
            "odia": "or"
        }
        
        lang_code = language_codes.get(target_language.lower(), "en")
        translation = translator.translate(text, dest=lang_code)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails

def find_relevant_law(law_type: str) -> Dict[str, Any]:
    """Find the most relevant law based on the law type."""
    if not law_type:
        return None
    
    law_type_lower = law_type.lower()
    
    for law in knowledge_base.get("laws", []):
        # Check if law_type is in the title or keywords
        if law_type_lower in law.get("title", "").lower() or any(law_type_lower in keyword.lower() for keyword in law.get("keywords", [])):
            return law
    
    return None

def get_document_checklist(case_type: str) -> List[str]:
    """Get document checklist for a specific case type."""
    if not case_type:
        return []
    
    case_type_lower = case_type.lower()
    
    for checklist in knowledge_base.get("document_checklists", []):
        if case_type_lower in checklist["case_type"].lower():
            return checklist["documents"]
    
    return []

def get_legal_procedure(procedure_type: str) -> Dict[str, Any]:
    """Get legal procedure details for a specific procedure type."""
    if not procedure_type:
        return None
    
    procedure_type_lower = procedure_type.lower()
    
    # Map common procedure types to procedure titles in the knowledge base
    procedure_mapping = {
        "fir": "Filing an FIR (First Information Report)",
        "domestic violence": "Filing a Domestic Violence Complaint",
        "sexual harassment": "Filing a Sexual Harassment Complaint at Workplace"
    }
    
    # Try direct mapping first
    for key, title in procedure_mapping.items():
        if key in procedure_type_lower:
            for procedure in knowledge_base.get("legal_procedures", []):
                if procedure["title"] == title:
                    return procedure
    
    # If no direct mapping, try to find a procedure with similar title
    for procedure in knowledge_base.get("legal_procedures", []):
        if procedure_type_lower in procedure["title"].lower():
            return procedure
    
    return None

class ActionProvideLawInfo(Action):
    def name(self) -> Text:
        return "action_provide_law_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        law_type = tracker.get_slot("law_type")
        language = tracker.get_slot("language") or "English"
        
        if not law_type:
            message = "What specific law or legal issue would you like information about?"
            dispatcher.utter_message(text=translate_text(message, language))
            return []
        
        law = find_relevant_law(law_type)
        
        if law:
            title = law.get("title", "")
            summary = law.get("summary", "")
            
            message = f"Here's information about {title}:\n\n{summary}"
            
            # Translate if needed
            if language.lower() != "english":
                message = translate_text(message, language)
            
            dispatcher.utter_message(text=message)
            return [SlotSet("law_type", law_type)]
        else:
            message = f"I'm sorry, I couldn't find specific information about {law_type}. Could you please try another term or be more specific?"
            dispatcher.utter_message(text=translate_text(message, language))
            return [SlotSet("law_type", None)]

class ActionProvideRights(Action):
    def name(self) -> Text:
        return "action_provide_rights"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        law_type = tracker.get_slot("law_type")
        language = tracker.get_slot("language") or "English"
        
        if not law_type:
            message = "What specific law would you like to know your rights under?"
            dispatcher.utter_message(text=translate_text(message, language))
            return []
        
        law = find_relevant_law(law_type)
        
        if law and "rights" in law and law["rights"]:
            title = law.get("title", "")
            rights = law.get("rights", [])
            
            rights_text = "\n- " + "\n- ".join(rights)
            message = f"Under the {title}, you have the following rights:{rights_text}"
            
            # Translate if needed
            if language.lower() != "english":
                message = translate_text(message, language)
            
            dispatcher.utter_message(text=message)
            return [SlotSet("law_type", law_type)]
        else:
            message = f"I'm sorry, I couldn't find specific rights information related to {law_type}. Could you please try another term or be more specific?"
            dispatcher.utter_message(text=translate_text(message, language))
            return [SlotSet("law_type", None)]

class ActionProvideProcedure(Action):
    def name(self) -> Text:
        return "action_provide_procedure"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        procedure_type = tracker.get_slot("procedure_type")
        language = tracker.get_slot("language") or "English"
        
        if not procedure_type:
            message = "What legal procedure would you like to know about?"
            dispatcher.utter_message(text=translate_text(message, language))
            return []
        
        procedure = get_legal_procedure(procedure_type)
        
        if procedure:
            title = procedure.get("title", "")
            steps = procedure.get("steps", [])
            notes = procedure.get("notes", "")
            
            steps_text = "\n1. " + "\n2. ".join(steps)
            message = f"Here's the procedure for {title}:{steps_text}"
            
            if notes:
                message += f"\n\nNote: {notes}"
            
            # Translate if needed
            if language.lower() != "english":
                message = translate_text(message, language)
            
            dispatcher.utter_message(text=message)
            return [SlotSet("procedure_type", procedure_type)]
        else:
            message = f"I'm sorry, I couldn't find specific procedure information for {procedure_type}. Could you please try another term or be more specific?"
            dispatcher.utter_message(text=translate_text(message, language))
            return [SlotSet("procedure_type", None)]

class ActionProvideDocuments(Action):
    def name(self) -> Text:
        return "action_provide_documents"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        case_type = tracker.get_slot("case_type")
        language = tracker.get_slot("language") or "English"
        
        if not case_type:
            message = "What type of case do you need a document checklist for?"
            dispatcher.utter_message(text=translate_text(message, language))
            return []
        
        documents = get_document_checklist(case_type)
        
        if documents:
            docs_text = "\n- " + "\n- ".join(documents)
            message = f"Here's the document checklist for {case_type} cases:{docs_text}"
            
            # Translate if needed
            if language.lower() != "english":
                message = translate_text(message, language)
            
            dispatcher.utter_message(text=message)
            return [SlotSet("case_type", case_type)]
        else:
            message = f"I'm sorry, I couldn't find a specific document checklist for {case_type} cases. Could you please try another case type or be more specific?"
            dispatcher.utter_message(text=translate_text(message, language))
            return [SlotSet("case_type", None)]

class ActionHandleEmergency(Action):
    def name(self) -> Text:
        return "action_handle_emergency"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        language = tracker.get_slot("language") or "English"
        
        emergency_contacts = knowledge_base.get("emergency_contacts", [])
        
        if emergency_contacts:
            contacts_text = "\n- " + "\n- ".join([f"{contact['name']}: {contact['number']}" for contact in emergency_contacts])
            message = f"This appears to be an emergency situation. Please contact one of the following emergency services immediately:{contacts_text}"
            
            # Translate if needed
            if language.lower() != "english":
                message = translate_text(message, language)
            
            dispatcher.utter_message(text=message)
        else:
            message = "This appears to be an emergency situation. Please contact the police at 100 immediately."
            dispatcher.utter_message(text=translate_text(message, language))
        
        return []

class ActionProvideContacts(Action):
    def name(self) -> Text:
        return "action_provide_contacts"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        language = tracker.get_slot("language") or "English"
        
        emergency_contacts = knowledge_base.get("emergency_contacts", [])
        
        if emergency_contacts:
            contacts_text = "\n- " + "\n- ".join([f"{contact['name']}: {contact['number']}" for contact in emergency_contacts])
            message = f"Here are important contact numbers that may help you:{contacts_text}"
            
            # Translate if needed
            if language.lower() != "english":
                message = translate_text(message, language)
            
            dispatcher.utter_message(text=message)
        else:
            message = "I'm sorry, I couldn't find any contact information at the moment."
            dispatcher.utter_message(text=translate_text(message, language))
        
        return []

class ActionChangeLanguage(Action):
    def name(self) -> Text:
        return "action_change_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        language = tracker.get_slot("language")
        
        if not language:
            message = "Which language would you prefer? I support English, Hindi, Bengali, Telugu, Marathi, Tamil, Urdu, Gujarati, Kannada, and Odia."
            dispatcher.utter_message(text=message)
            return []
        
        supported_languages = knowledge_base.get("languages", ["English"])
        
        if language.capitalize() in supported_languages:
            message = f"Language changed to {language.capitalize()}. How can I help you?"
            # Translate the confirmation message to the new language
            translated_message = translate_text(message, language)
            dispatcher.utter_message(text=translated_message)
            return [SlotSet("language", language.capitalize())]
        else:
            message = f"I'm sorry, I don't support {language} yet. I currently support English, Hindi, Bengali, Telugu, Marathi, Tamil, Urdu, Gujarati, Kannada, and Odia."
            dispatcher.utter_message(text=message)
            return [SlotSet("language", "English")]