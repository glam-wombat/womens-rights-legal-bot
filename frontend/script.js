document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const voiceInputBtn = document.getElementById('voice-input-btn');
    const emergencyBtn = document.getElementById('emergency-btn');
    const languageSelector = document.getElementById('language');
    const modal = document.getElementById('flowchart-modal');
    const closeModal = document.querySelector('.close');
    const flowchartTitle = document.getElementById('flowchart-title');
    const flowchartContainer = document.getElementById('flowchart-container');

    // API URL - Change this to your actual backend URL when deployed
    const API_URL = 'http://localhost:8000';
    
    // Current language
    let currentLanguage = 'English';

    // Initialize the chat
    function initChat() {
        // Load supported languages
        fetch(`${API_URL}/languages`)
            .then(response => response.json())
            .then(data => {
                // Populate language selector if needed
                // (Already done in HTML for this implementation)
            })
            .catch(error => console.error('Error fetching languages:', error));

        // Set up event listeners
        sendBtn.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        voiceInputBtn.addEventListener('click', startVoiceInput);
        emergencyBtn.addEventListener('click', handleEmergency);
        languageSelector.addEventListener('change', changeLanguage);
        closeModal.addEventListener('click', () => modal.style.display = 'none');
        window.addEventListener('click', function(event) {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    }

    // Send user message to the backend
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;

        // Add user message to chat
        addMessageToChat('user', message);
        userInput.value = '';

        // Show typing indicator
        const typingIndicator = addTypingIndicator();

        // Send message to backend
        fetch(`${API_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: message,
                language: currentLanguage
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            chatMessages.removeChild(typingIndicator);

            // Process the response
            processResponse(data);
        })
        .catch(error => {
            console.error('Error:', error);
            chatMessages.removeChild(typingIndicator);
            addMessageToChat('bot', 'Sorry, I encountered an error. Please try again later.');
        });
    }

    // Process the response from the backend
    function processResponse(data) {
        // Add the main response
        addMessageToChat('bot', data.response);

        // Handle emergency contacts if present
        if (data.is_emergency && data.emergency_contacts) {
            const contactsMessage = document.createElement('div');
            contactsMessage.className = 'message bot';
            const contactsContent = document.createElement('div');
            contactsContent.className = 'message-content';

            const contactsList = document.createElement('ul');
            data.emergency_contacts.forEach(contact => {
                const contactItem = document.createElement('li');
                contactItem.textContent = contact;
                contactsList.appendChild(contactItem);
            });

            contactsContent.appendChild(contactsList);
            contactsMessage.appendChild(contactsContent);
            chatMessages.appendChild(contactsMessage);
            scrollToBottom();
        }

        // Handle document checklist if present
        if (data.document_checklist) {
            const checklistMessage = document.createElement('div');
            checklistMessage.className = 'message bot';
            const checklistContent = document.createElement('div');
            checklistContent.className = 'message-content';

            const checklistTitle = document.createElement('p');
            checklistTitle.textContent = 'Required Documents:';
            checklistTitle.style.fontWeight = 'bold';
            checklistContent.appendChild(checklistTitle);

            const documentsList = document.createElement('ul');
            data.document_checklist.forEach(doc => {
                const docItem = document.createElement('li');
                docItem.textContent = doc;
                documentsList.appendChild(docItem);
            });

            checklistContent.appendChild(documentsList);
            checklistMessage.appendChild(checklistContent);
            chatMessages.appendChild(checklistMessage);
            scrollToBottom();
        }

        // Handle legal procedure if present
        if (data.legal_procedure) {
            const procedureMessage = document.createElement('div');
            procedureMessage.className = 'message bot';
            const procedureContent = document.createElement('div');
            procedureContent.className = 'message-content';

            const procedureTitle = document.createElement('p');
            procedureTitle.textContent = data.legal_procedure.title;
            procedureTitle.style.fontWeight = 'bold';
            procedureContent.appendChild(procedureTitle);

            const stepsList = document.createElement('ol');
            data.legal_procedure.steps.forEach(step => {
                const stepItem = document.createElement('li');
                stepItem.textContent = step;
                stepsList.appendChild(stepItem);
            });

            procedureContent.appendChild(stepsList);

            if (data.legal_procedure.notes) {
                const notes = document.createElement('p');
                notes.textContent = `Note: ${data.legal_procedure.notes}`;
                notes.style.fontStyle = 'italic';
                notes.style.marginTop = '10px';
                procedureContent.appendChild(notes);
            }

            // Add a button to view the flowchart
            const flowchartBtn = document.createElement('button');
            flowchartBtn.textContent = 'View Flowchart';
            flowchartBtn.style.marginTop = '10px';
            flowchartBtn.style.padding = '5px 10px';
            flowchartBtn.style.backgroundColor = '#8e44ad';
            flowchartBtn.style.color = 'white';
            flowchartBtn.style.border = 'none';
            flowchartBtn.style.borderRadius = '5px';
            flowchartBtn.style.cursor = 'pointer';
            
            flowchartBtn.addEventListener('click', function() {
                showFlowchart(data.legal_procedure);
            });
            
            procedureContent.appendChild(flowchartBtn);
            procedureMessage.appendChild(procedureContent);
            chatMessages.appendChild(procedureMessage);
            scrollToBottom();
        }

        // Handle law information if present
        if (data.law_title && data.law_summary) {
            const lawMessage = document.createElement('div');
            lawMessage.className = 'message bot';
            const lawContent = document.createElement('div');
            lawContent.className = 'message-content';

            const lawTitle = document.createElement('p');
            lawTitle.textContent = data.law_title;
            lawTitle.style.fontWeight = 'bold';
            lawContent.appendChild(lawTitle);

            const lawSummary = document.createElement('p');
            lawSummary.textContent = data.law_summary;
            lawContent.appendChild(lawSummary);

            lawMessage.appendChild(lawContent);
            chatMessages.appendChild(lawMessage);
            scrollToBottom();
        }

        // Handle rights if present
        if (data.rights && data.rights.length > 0) {
            const rightsMessage = document.createElement('div');
            rightsMessage.className = 'message bot';
            const rightsContent = document.createElement('div');
            rightsContent.className = 'message-content';

            const rightsTitle = document.createElement('p');
            rightsTitle.textContent = 'Your Rights:';
            rightsTitle.style.fontWeight = 'bold';
            rightsContent.appendChild(rightsTitle);

            const rightsList = document.createElement('ul');
            data.rights.forEach(right => {
                const rightItem = document.createElement('li');
                rightItem.textContent = right;
                rightsList.appendChild(rightItem);
            });

            rightsContent.appendChild(rightsList);
            rightsMessage.appendChild(rightsContent);
            chatMessages.appendChild(rightsMessage);
            scrollToBottom();
        }
    }

    // Add a message to the chat
    function addMessageToChat(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        // Handle multi-line messages
        const paragraphs = message.split('\n').filter(p => p.trim() !== '');
        paragraphs.forEach(paragraph => {
            const p = document.createElement('p');
            p.textContent = paragraph;
            contentDiv.appendChild(p);
        });

        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    // Add typing indicator
    function addTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing-indicator';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = '<p>Typing<span>.</span><span>.</span><span>.</span></p>';

        typingDiv.appendChild(contentDiv);
        chatMessages.appendChild(typingDiv);
        scrollToBottom();

        return typingDiv;
    }

    // Scroll to the bottom of the chat
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Handle emergency button click
    function handleEmergency() {
        // Add user emergency message
        addMessageToChat('user', 'EMERGENCY HELP NEEDED');

        // Show typing indicator
        const typingIndicator = addTypingIndicator();

        // Send emergency request to backend
        fetch(`${API_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: 'emergency help',
                language: currentLanguage
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            chatMessages.removeChild(typingIndicator);

            // Process the response
            processResponse(data);
        })
        .catch(error => {
            console.error('Error:', error);
            chatMessages.removeChild(typingIndicator);
            addMessageToChat('bot', 'For immediate emergency assistance, please call the Women Helpline (All India) at 1091 or Police at 100.');
        });
    }

    // Start voice input
    function startVoiceInput() {
        // Check if browser supports speech recognition
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();

            // Set language based on current selection
            const languageCodes = {
                'English': 'en-IN',
                'Hindi': 'hi-IN',
                'Bengali': 'bn-IN',
                'Telugu': 'te-IN',
                'Marathi': 'mr-IN',
                'Tamil': 'ta-IN',
                'Urdu': 'ur-IN',
                'Gujarati': 'gu-IN',
                'Kannada': 'kn-IN',
                'Odia': 'or-IN'
            };

            recognition.lang = languageCodes[currentLanguage] || 'en-IN';
            recognition.interimResults = false;

            // Change microphone button color to indicate recording
            voiceInputBtn.style.backgroundColor = '#e74c3c';
            voiceInputBtn.innerHTML = '<i class="fas fa-microphone-slash"></i>';

            recognition.start();

            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                userInput.value = transcript;
                // Reset microphone button
                voiceInputBtn.style.backgroundColor = '#8e44ad';
                voiceInputBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            };

            recognition.onerror = function(event) {
                console.error('Speech recognition error:', event.error);
                // Reset microphone button
                voiceInputBtn.style.backgroundColor = '#8e44ad';
                voiceInputBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            };

            recognition.onend = function() {
                // Reset microphone button
                voiceInputBtn.style.backgroundColor = '#8e44ad';
                voiceInputBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            };
        } else {
            alert('Your browser does not support speech recognition. Please try using a different browser like Chrome.');
        }
    }

    // Change language
    function changeLanguage() {
        currentLanguage = languageSelector.value;
        
        // Notify the user about language change
        addMessageToChat('bot', `Language changed to ${currentLanguage}`);
        
        // Send language change request to backend
        fetch(`${API_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: `change language to ${currentLanguage}`,
                language: currentLanguage
            })
        })
        .then(response => response.json())
        .then(data => {
            // Process the response if needed
        })
        .catch(error => {
            console.error('Error changing language:', error);
        });
    }

    // Show flowchart in modal
    function showFlowchart(procedure) {
        flowchartTitle.textContent = procedure.title;
        
        // Create a simple flowchart using HTML
        let flowchartHTML = '<div class="flowchart">';
        flowchartHTML += '<div class="flowchart-start">Start</div>';
        
        procedure.steps.forEach((step, index) => {
            flowchartHTML += `<div class="flowchart-arrow">↓</div>`;
            flowchartHTML += `<div class="flowchart-step">${index + 1}. ${step}</div>`;
        });
        
        flowchartHTML += '<div class="flowchart-arrow">↓</div>';
        flowchartHTML += '<div class="flowchart-end">End</div>';
        flowchartHTML += '</div>';
        
        flowchartContainer.innerHTML = flowchartHTML;
        
        // Add some inline styles for the flowchart
        const style = document.createElement('style');
        style.textContent = `
            .flowchart {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 20px;
            }
            .flowchart-start, .flowchart-end {
                background-color: #8e44ad;
                color: white;
                padding: 10px 20px;
                border-radius: 20px;
                margin: 10px 0;
                text-align: center;
                width: 100px;
            }
            .flowchart-step {
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                padding: 15px;
                border-radius: 5px;
                margin: 10px 0;
                text-align: left;
                width: 80%;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .flowchart-arrow {
                font-size: 24px;
                margin: 5px 0;
                color: #8e44ad;
            }
        `;
        document.head.appendChild(style);
        
        modal.style.display = 'block';
    }

    // Initialize the chat
    initChat();
});