# Development Guide for Women's Rights Legal Assistance Bot

This guide provides instructions for setting up and running the Women's Rights Legal Assistance Bot locally for development and testing.

## Prerequisites

- Python 3.8 or higher
- Node.js and npm (optional, for running a local HTTP server for the frontend)
- Git

## Setup Instructions

### 1. Clone the Repository

If you're working with a remote repository, clone it first:

```bash
git clone https://github.com/yourusername/womens-rights-legal-bot.git
cd womens-rights-legal-bot
```

Or if you're starting from the local files:

```bash
cd indi_Law_bot_
```

### 2. Set Up Python Virtual Environment

Create and activate a virtual environment:

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Running the Backend

Start the FastAPI backend server:

```bash
cd backend
uvicorn main:app --reload
```

The backend will be available at http://localhost:8000

### 5. Running the Frontend

You can serve the frontend using any HTTP server. Here are a few options:

#### Using Python's built-in HTTP server

```bash
cd frontend
python -m http.server 8080
```

#### Using Node.js http-server (if installed)

```bash
cd frontend
npx http-server -p 8080
```

The frontend will be available at http://localhost:8080

### 6. Setting Up and Running Rasa

To set up and run the Rasa NLU server:

#### Train the Rasa model

```bash
cd rasa
rasa train
```

#### Run the Rasa server

```bash
rasa run --enable-api --cors "*" --port 5005
```

#### Run the Rasa actions server (in a separate terminal)

```bash
cd rasa
rasa run actions
```

## Development Workflow

### Backend Development

1. Make changes to the FastAPI backend code in the `backend` directory
2. The server will automatically reload if you're using the `--reload` flag with uvicorn
3. Test your changes using the API endpoints

### Frontend Development

1. Make changes to the HTML, CSS, and JavaScript files in the `frontend` directory
2. Refresh your browser to see the changes
3. Use the browser's developer tools to debug any issues

### Rasa NLP Development

1. Make changes to the Rasa configuration, domain, or training data in the `rasa` directory
2. Retrain the model with `rasa train`
3. Restart the Rasa server to apply the changes

### Knowledge Base Updates

1. Edit the `data/laws.json` file to update or add new legal information
2. Restart the backend server if necessary

## Testing

### Manual Testing

1. Use the frontend interface to test the bot's responses
2. Test different types of queries and edge cases
3. Verify that emergency contacts, document checklists, and legal procedures are displayed correctly

### API Testing

You can test the backend API endpoints directly using tools like curl, Postman, or the built-in FastAPI documentation.

Access the FastAPI documentation at http://localhost:8000/docs

## Debugging

### Backend Debugging

- Check the terminal running the backend server for error messages
- Use Python's debugging tools or add print statements to debug issues

### Frontend Debugging

- Use the browser's developer tools (F12) to debug JavaScript issues
- Check the Console tab for error messages
- Use the Network tab to monitor API requests and responses

### Rasa Debugging

- Check the terminal running the Rasa server for error messages
- Use the Rasa shell for interactive debugging:

```bash
rasa shell
```

## Code Structure

### Backend

- `backend/main.py`: Main FastAPI application
- `backend/rasa_connector.py`: Connector for integrating with Rasa NLU

### Frontend

- `frontend/index.html`: Main HTML file
- `frontend/styles.css`: CSS styles
- `frontend/script.js`: JavaScript for the chat interface

### Rasa

- `rasa/config.yml`: Rasa configuration
- `rasa/domain.yml`: Domain definition
- `rasa/data/`: Training data
- `rasa/actions/`: Custom actions

### Data

- `data/laws.json`: Knowledge base with legal information

## Contributing

1. Create a new branch for your feature or bugfix
2. Make your changes
3. Test thoroughly
4. Commit your changes with descriptive commit messages
5. Push your branch and create a pull request

## Best Practices

1. Follow the existing code style and conventions
2. Document your code with comments
3. Update documentation when making significant changes
4. Test your changes thoroughly before committing
5. Keep the knowledge base accurate and up-to-date