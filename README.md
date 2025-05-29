# Women's Rights Legal Assistance Bot for Indian Judicial System

A free, open-source chatbot that provides accurate legal information for women in India using exclusively free technologies and APIs.

## Project Overview

This bot aims to empower women with knowledge about their legal rights and provide guidance on legal procedures within the Indian judicial system. It uses natural language processing to understand user queries and provides relevant information about women-centric laws, rights, and procedures.

## Core Features

- **NLP Engine**: Uses Rasa Open Source for intent classification and hierarchical legal topic identification
- **Knowledge Base**: Structured women-centric laws in JSON format
- **Emergency Contact Display**: Quick access to emergency contacts for urgent situations
- **Document Checklist Generator**: Provides lists of required documents for different case types
- **Legal Procedure Flowcharts**: Visual guides for legal procedures like filing an FIR
- **Multilingual Support**: Available in 10 Indian languages using Google Translate API

## Technical Implementation

### Backend (Python)
- FastAPI for API endpoints
- Rasa Open Source for NLP
- JSON-based knowledge database

### Frontend
- Minimalist chat interface with HTML/JS
- Voice input via Web Speech API
- Responsive design for low-bandwidth areas

### Hosting
- Frontend: GitHub Pages
- Backend: PythonAnywhere (free tier)
- Data: Version-controlled JSON in GitHub repo

## Constraints

- Zero-cost implementation (only free-tier services)
- Mandatory privacy protection (no personal data storage)
- Accuracy safeguards:
  - Monthly legal data audits
  - Community verification mechanism
  - Timestamped legal references

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js and npm (for frontend development)

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/womens-rights-legal-bot.git
   cd womens-rights-legal-bot
   ```

2. Set up the backend
   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up Rasa
   ```
   cd rasa
   pip install -r requirements.txt
   rasa train
   ```

4. Set up the frontend
   ```
   cd frontend
   npm install
   ```

### Running the Application

1. Start the backend server
   ```
   cd backend
   uvicorn main:app --reload
   ```

2. Start the Rasa server
   ```
   cd rasa
   rasa run --enable-api
   ```

3. Start the frontend development server
   ```
   cd frontend
   npm start
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This bot provides general legal information and is not a substitute for professional legal advice. Always consult with a qualified legal professional for specific legal matters.