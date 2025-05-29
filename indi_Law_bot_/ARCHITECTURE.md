# System Architecture: Women's Rights Legal Assistance Bot

This document describes the architecture of the Women's Rights Legal Assistance Bot, explaining how different components interact to provide legal assistance.

## Architecture Overview

```
+----------------------------------+
|           Frontend               |
|  (HTML/CSS/JS - GitHub Pages)   |
+----------------------------------+
              |
              | HTTP/HTTPS
              |
+----------------------------------+
|           Backend                |
|      (FastAPI - PythonAnywhere) |
+----------------------------------+
              |         \
              |          \
              |           \
+---------------+    +------------------+
|  Rasa NLU     |    |  Knowledge Base |
| (PythonAnywhere)|   |   (laws.json)   |
+---------------+    +------------------+
```

## Component Details

### 1. Frontend

**Technology**: HTML, CSS, JavaScript
**Hosting**: GitHub Pages (free tier)

**Key Components**:
- Chat interface with message history
- Voice input using Web Speech API
- Language selector for multilingual support
- Emergency help button
- Responsive design for various devices
- Flowchart modal for legal procedures

**Responsibilities**:
- Provide user interface for interaction
- Handle voice input and text-to-speech
- Send user queries to backend API
- Display bot responses in appropriate format
- Support language switching
- Render emergency contacts, document checklists, and legal procedures

### 2. Backend

**Technology**: Python with FastAPI
**Hosting**: PythonAnywhere (free tier)

**Key Components**:
- FastAPI application (main.py)
- Rasa connector (rasa_connector.py)
- CORS middleware for cross-origin requests
- Translation service using googletrans

**Responsibilities**:
- Process incoming user queries
- Identify emergency requests
- Connect with Rasa NLU for intent classification
- Retrieve relevant information from knowledge base
- Translate responses to requested language
- Format and return structured responses

### 3. Rasa NLU

**Technology**: Rasa Open Source
**Hosting**: PythonAnywhere (free tier)

**Key Components**:
- NLU pipeline (config.yml)
- Domain definition (domain.yml)
- Training data (nlu.yml)
- Conversation flows (stories.yml)
- Conversation rules (rules.yml)
- Custom actions (actions.py)

**Responsibilities**:
- Classify user intents (e.g., ask_law_info, report_emergency)
- Extract entities (e.g., law_type, case_type)
- Maintain conversation context
- Execute custom actions based on user intent

### 4. Knowledge Base

**Technology**: JSON data structure
**Storage**: GitHub repository (version-controlled)

**Key Components**:
- Legal information on women-centric laws
- Rights and protections under each law
- Emergency contacts
- Document checklists for different case types
- Legal procedures with step-by-step instructions

**Structure**:
```json
{
  "laws": [
    {
      "title": "Law Title",
      "keywords": ["keyword1", "keyword2"],
      "summary": "Law summary",
      "rights": ["Right 1", "Right 2"],
      "sections": ["Section details"],
      "procedures": ["Procedure steps"],
      "required_documents": ["Document 1", "Document 2"],
      "emergency_contacts": ["Contact 1", "Contact 2"]
    }
  ],
  "emergency_contacts": ["General emergency contacts"],
  "document_checklists": {"case_type": ["Documents"]},
  "legal_procedures": {"procedure_type": {"steps": ["Steps"]}},
  "supported_languages": ["Language codes"]
}
```

## Data Flow

### Query Processing Flow

1. **User Input**:
   - User enters a query via text or voice in the frontend
   - Frontend captures the input and sends it to the backend API

2. **Backend Processing**:
   - Backend receives the query
   - Checks for emergency keywords
   - If emergency is detected, returns emergency contacts immediately
   - Otherwise, processes the query further

3. **NLP Processing** (two options):
   - **Option A - Basic Keyword Matching**:
     - Backend searches for keywords in the query
     - Matches keywords against the knowledge base
     - Retrieves relevant information
   
   - **Option B - Rasa NLU Processing**:
     - Backend sends the query to Rasa NLU
     - Rasa classifies the intent and extracts entities
     - Rasa executes custom actions if needed
     - Returns structured response

4. **Knowledge Retrieval**:
   - Based on identified intent and entities
   - Retrieves relevant law information, rights, procedures, or document checklists
   - Formats the information for display

5. **Translation** (if needed):
   - Translates the response to the user's selected language
   - Uses googletrans library for translation

6. **Response Delivery**:
   - Backend sends the formatted response to the frontend
   - Frontend displays the response in the chat interface
   - Special formatting for emergency contacts, document checklists, and procedures

## Multilingual Support

The system supports 10 Indian languages through the following mechanism:

1. Frontend maintains the current language selection
2. User queries are sent to the backend in their original language
3. Backend processes the query in the original language or translates to English for processing
4. Response is translated back to the user's selected language before sending to frontend
5. Frontend displays the translated response

## Privacy and Security

1. **No Personal Data Storage**:
   - No user conversations are stored
   - No personal identifiers are collected
   - Session data is temporary and client-side only

2. **Stateless Backend**:
   - Each request is processed independently
   - No user state is maintained between requests

3. **Disclaimer**:
   - Clear disclaimer that the bot provides information, not legal advice
   - Recommendation to consult qualified legal professionals

## Scalability Considerations

While the current architecture uses free-tier services with limitations, it is designed to be scalable:

1. **Horizontal Scaling**:
   - Backend can be deployed to multiple instances
   - Stateless design facilitates load balancing

2. **Knowledge Base Expansion**:
   - JSON structure allows for easy addition of new laws and information
   - Version control enables collaborative updates

3. **Language Support**:
   - Architecture supports adding more languages
   - Translation mechanism is language-agnostic

## Limitations

1. **Free-Tier Constraints**:
   - PythonAnywhere has CPU and bandwidth limitations
   - GitHub Pages has storage and bandwidth limits

2. **Translation Quality**:
   - Free translation services may have quality limitations
   - Legal terminology may not always translate accurately

3. **NLP Accuracy**:
   - Intent classification depends on training data quality
   - Complex legal queries may be misinterpreted

## Future Architecture Enhancements

1. **Caching Layer**:
   - Add Redis or similar for response caching
   - Reduce redundant processing of common queries

2. **Advanced NLP**:
   - Integrate more sophisticated NLP models
   - Implement contextual understanding

3. **Database Integration**:
   - Move from static JSON to a database for larger knowledge base
   - Enable more complex queries and relationships

4. **User Feedback Loop**:
   - Add feedback collection mechanism
   - Use feedback to improve responses

5. **API Gateway**:
   - Add API gateway for better security and rate limiting
   - Enable service composition for more complex features