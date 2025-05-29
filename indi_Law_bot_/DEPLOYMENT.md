# Deployment Guide for Women's Rights Legal Assistance Bot

This guide provides instructions for deploying the Women's Rights Legal Assistance Bot using free-tier services.

## Prerequisites

- GitHub account
- PythonAnywhere account (free tier)
- Basic knowledge of Git and command line

## Deployment Steps

### 1. Set Up GitHub Repository

1. Create a new GitHub repository
2. Push your local code to the repository:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/womens-rights-legal-bot.git
git push -u origin main
```

### 2. Deploy Frontend on GitHub Pages

1. In your GitHub repository, go to Settings > Pages
2. Under "Source", select the branch you want to deploy (e.g., main)
3. Select the `/frontend` folder as the source
4. Click Save
5. GitHub Pages will provide you with a URL where your frontend is deployed

### 3. Deploy Backend on PythonAnywhere

1. Sign up for a free PythonAnywhere account at https://www.pythonanywhere.com/
2. Go to the Dashboard and click on "Web" tab
3. Click "Add a new web app"
4. Choose "Manual configuration" and select Python 3.8
5. Set the path to your web app to `/home/yourusername/womens-rights-legal-bot/backend/main.py`

#### Clone your repository on PythonAnywhere

1. Go to the "Consoles" tab and start a new Bash console
2. Clone your GitHub repository:

```bash
git clone https://github.com/yourusername/womens-rights-legal-bot.git
```

#### Set up a virtual environment and install dependencies

```bash
cd womens-rights-legal-bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Configure the WSGI file

1. Go back to the "Web" tab
2. Click on the WSGI configuration file link
3. Replace the content with the following:

```python
import sys
import os

path = '/home/yourusername/womens-rights-legal-bot'
if path not in sys.path:
    sys.path.append(path)

from backend.main import app as application
```

4. Save the file

#### Configure allowed hosts

1. Edit your `backend/main.py` file to allow requests from your GitHub Pages domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourusername.github.io"],  # Replace with your GitHub Pages URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. Reload your web app from the PythonAnywhere dashboard

### 4. Deploy Rasa on PythonAnywhere (Optional)

If you want to use Rasa for more advanced NLP capabilities:

1. In the PythonAnywhere Bash console, navigate to your project directory
2. Install Rasa in your virtual environment:

```bash
cd womens-rights-legal-bot
source venv/bin/activate
pip install rasa
```

3. Train your Rasa model:

```bash
cd rasa
rasa train
```

4. Set up a scheduled task to run Rasa server:

- Go to the "Tasks" tab on PythonAnywhere
- Add a new scheduled task that runs daily
- Command to run: `/home/yourusername/womens-rights-legal-bot/venv/bin/rasa run --enable-api --cors "*" --port 5005`

### 5. Update Frontend Configuration

1. Edit the `frontend/script.js` file to point to your PythonAnywhere backend:

```javascript
// Change this line
const API_URL = 'https://yourusername.pythonanywhere.com';
```

2. Commit and push the changes to GitHub:

```bash
git add frontend/script.js
git commit -m "Update API URL for production"
git push
```

## Maintenance and Updates

### Updating the Application

1. Make changes to your local repository
2. Commit and push to GitHub
3. For backend updates, pull the changes on PythonAnywhere:

```bash
cd womens-rights-legal-bot
git pull
```

4. Reload your web app from the PythonAnywhere dashboard

### Updating the Knowledge Base

1. Edit the `data/laws.json` file with new or updated legal information
2. Commit and push to GitHub
3. Pull the changes on PythonAnywhere as described above

## Monitoring and Troubleshooting

### Checking Logs on PythonAnywhere

1. Go to the "Web" tab on PythonAnywhere
2. Click on the "Log files" links to view error logs and access logs

### Common Issues and Solutions

#### CORS Errors

If you see CORS errors in your browser console:

1. Ensure your frontend is using the correct backend URL
2. Check that your backend has the correct CORS configuration with your frontend domain

#### 502 Bad Gateway

If you get a 502 error:

1. Check your WSGI configuration file
2. Ensure all dependencies are installed in your virtual environment
3. Check the error logs for specific issues

## Limitations of Free Tier

- PythonAnywhere free tier has CPU and bandwidth limitations
- The application may be put to sleep after periods of inactivity
- Limited storage space for your data

For a production environment with higher traffic, consider upgrading to paid tiers or using alternative hosting solutions.