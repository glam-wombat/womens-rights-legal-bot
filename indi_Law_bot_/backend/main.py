from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os
import requests
from googletrans import Translator

app = FastAPI(title="Women's Rights Legal Assistance Bot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the knowledge base
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
with open(os.path.join(data_dir, "laws.json"), "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# Initialize translator
translator = Translator()

# Define request and response models
class QueryRequest(BaseModel):
    query: str
    language: str = "English"

class EmergencyContact(BaseModel):
    name: str
    number: str
    description: str

class DocumentChecklist(BaseModel):
    case_type: str
    documents: List[str]

class LegalProcedure(BaseModel):
    title: str
    steps: List[str]
    notes: Optional[str] = None

class QueryResponse(BaseModel):
    response: str
    law_title: Optional[str] = None
    law_summary: Optional[str] = None
    rights: Optional[List[str]] = None
    sections: Optional[List[Dict[str, Any]]] = None
    procedures: Optional[List[Dict[str, Any]]] = None
    documents_required: Optional[List[str]] = None
    emergency_contacts: Optional[List[str]] = None
    is_emergency: bool = False
    document_checklist: Optional[List[str]] = None
    legal_procedure: Optional[Dict[str, Any]] = None

# Helper functions
def is_emergency(query: str) -> bool:
    """Check if the query contains emergency keywords."""
    emergency_keywords = ["emergency", "urgent", "help", "danger", "threatened", "immediate", "crisis"]
    return any(keyword in query.lower() for keyword in emergency_keywords)

def get_emergency_contacts() -> List[EmergencyContact]:
    """Get all emergency contacts from the knowledge base."""
    return knowledge_base.get("emergency_contacts", [])

def get_document_checklist(case_type: str) -> Optional[List[str]]:
    """Get document checklist for a specific case type."""
    for checklist in knowledge_base.get("document_checklists", []):
        if checklist["case_type"].lower() == case_type.lower():
            return checklist["documents"]
    return None

def get_legal_procedure(procedure_title: str) -> Optional[Dict[str, Any]]:
    """Get legal procedure details for a specific procedure."""
    for procedure in knowledge_base.get("legal_procedures", []):
        if procedure["title"].lower() == procedure_title.lower():
            return procedure
    return None

def find_relevant_law(query: str) -> Optional[Dict[str, Any]]:
    """Find the most relevant law based on the query keywords."""
    query_words = set(query.lower().split())
    best_match = None
    highest_score = 0
    
    for law in knowledge_base.get("laws", []):
        # Check for keyword matches
        score = sum(1 for keyword in law.get("keywords", []) if keyword.lower() in query.lower())
        
        # Check for word matches in title and summary
        title_words = set(law.get("title", "").lower().split())
        summary_words = set(law.get("summary", "").lower().split())
        
        score += len(query_words.intersection(title_words)) * 2  # Title matches have higher weight
        score += len(query_words.intersection(summary_words))
        
        if score > highest_score:
            highest_score = score
            best_match = law
    
    # Only return if we have a reasonable match
    if highest_score > 0:
        return best_match
    return None

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

# API endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to the Women's Rights Legal Assistance Bot API"}

@app.post("/ask", response_model=QueryResponse)
async def legal_query(request: QueryRequest):
    query = request.query
    language = request.language
    
    # Check if it's an emergency
    emergency_status = is_emergency(query)
    
    # Initialize response
    response_data = {
        "response": "",
        "is_emergency": emergency_status
    }
    
    # Handle emergency queries
    if emergency_status:
        emergency_contacts = get_emergency_contacts()
        response_data["response"] = "This appears to be an emergency situation. Please contact one of the following emergency services immediately:"
        response_data["emergency_contacts"] = [f"{contact['name']}: {contact['number']}" for contact in emergency_contacts]
        
        # Translate response if needed
        if language.lower() != "english":
            response_data["response"] = translate_text(response_data["response"], language)
            response_data["emergency_contacts"] = [translate_text(contact, language) for contact in response_data["emergency_contacts"]]
        
        return response_data
    
    # Check for document checklist request
    if "document" in query.lower() and "checklist" in query.lower():
        # Extract case type from query
        case_types = ["domestic violence", "sexual harassment", "dowry harassment", "divorce", "maintenance"]
        found_case_type = None
        
        for case_type in case_types:
            if case_type in query.lower():
                found_case_type = case_type
                break
        
        if found_case_type:
            checklist = get_document_checklist(found_case_type)
            if checklist:
                response_data["response"] = f"Here is the document checklist for {found_case_type} cases:"
                response_data["document_checklist"] = checklist
                
                # Translate response if needed
                if language.lower() != "english":
                    response_data["response"] = translate_text(response_data["response"], language)
                    response_data["document_checklist"] = [translate_text(doc, language) for doc in response_data["document_checklist"]]
                
                return response_data
    
    # Check for legal procedure request
    if "procedure" in query.lower() or "process" in query.lower() or "how to" in query.lower():
        procedure_types = ["filing an fir", "domestic violence complaint", "sexual harassment complaint"]
        found_procedure = None
        
        for procedure in procedure_types:
            if procedure in query.lower():
                found_procedure = procedure
                break
        
        if found_procedure:
            procedure_info = None
            
            # Map query terms to procedure titles in the knowledge base
            procedure_mapping = {
                "filing an fir": "Filing an FIR (First Information Report)",
                "domestic violence complaint": "Filing a Domestic Violence Complaint",
                "sexual harassment complaint": "Filing a Sexual Harassment Complaint at Workplace"
            }
            
            mapped_procedure = procedure_mapping.get(found_procedure)
            if mapped_procedure:
                procedure_info = get_legal_procedure(mapped_procedure)
            
            if procedure_info:
                response_data["response"] = f"Here is the procedure for {mapped_procedure}:"
                response_data["legal_procedure"] = procedure_info
                
                # Translate response if needed
                if language.lower() != "english":
                    response_data["response"] = translate_text(response_data["response"], language)
                    response_data["legal_procedure"]["title"] = translate_text(procedure_info["title"], language)
                    response_data["legal_procedure"]["steps"] = [translate_text(step, language) for step in procedure_info["steps"]]
                    if procedure_info.get("notes"):
                        response_data["legal_procedure"]["notes"] = translate_text(procedure_info["notes"], language)
                
                return response_data
    
    # Find relevant law
    relevant_law = find_relevant_law(query)
    
    if relevant_law:
        response_data["response"] = f"Based on your query, I found information about the {relevant_law['title']}:"
        response_data["law_title"] = relevant_law["title"]
        response_data["law_summary"] = relevant_law["summary"]
        response_data["rights"] = relevant_law.get("rights", [])
        response_data["sections"] = relevant_law.get("sections", [])
        response_data["procedures"] = relevant_law.get("procedures", [])
        response_data["documents_required"] = relevant_law.get("documents_required", [])
        response_data["emergency_contacts"] = [f"{contact}" for contact in relevant_law.get("emergency_contacts", [])]
        
        # Translate response if needed
        if language.lower() != "english":
            response_data["response"] = translate_text(response_data["response"], language)
            response_data["law_title"] = translate_text(response_data["law_title"], language)
            response_data["law_summary"] = translate_text(response_data["law_summary"], language)
            response_data["rights"] = [translate_text(right, language) for right in response_data["rights"]]
            
            for section in response_data["sections"]:
                section["title"] = translate_text(section["title"], language)
                section["content"] = translate_text(section["content"], language)
            
            for procedure in response_data["procedures"]:
                procedure["title"] = translate_text(procedure["title"], language)
                procedure["steps"] = [translate_text(step, language) for step in procedure["steps"]]
            
            response_data["documents_required"] = [translate_text(doc, language) for doc in response_data["documents_required"]]
            response_data["emergency_contacts"] = [translate_text(contact, language) for contact in response_data["emergency_contacts"]]
    else:
        # No relevant law found
        response_data["response"] = "I'm sorry, I couldn't find specific legal information related to your query. Please try rephrasing your question or consult with a legal professional for personalized advice."
        
        # Translate response if needed
        if language.lower() != "english":
            response_data["response"] = translate_text(response_data["response"], language)
    
    # Add disclaimer
    disclaimer = "\n\nDisclaimer: This information is provided for general guidance only and is not legal advice. Please consult with a qualified legal professional for specific legal matters."
    response_data["response"] += translate_text(disclaimer, language) if language.lower() != "english" else disclaimer
    
    return response_data

@app.get("/languages")
def get_supported_languages():
    return {"languages": knowledge_base.get("languages", ["English"])}

@app.get("/emergency-contacts")
def get_all_emergency_contacts():
    return {"emergency_contacts": knowledge_base.get("emergency_contacts", [])}

@app.get("/document-checklists")
def get_all_document_checklists():
    return {"document_checklists": knowledge_base.get("document_checklists", [])}

@app.get("/legal-procedures")
def get_all_legal_procedures():
    return {"legal_procedures": knowledge_base.get("legal_procedures", [])}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)