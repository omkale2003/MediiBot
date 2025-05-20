// script.js

let currentChat = []; // Stores current conversation messages

// Initialize when page loads
window.addEventListener('DOMContentLoaded', () => {
    loadChatHistory();
    setupEventListeners();
});

// Handler functions
function handleSendClick() { sendMessage(); }
function handleKeyPress(e) { 
    if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
    }
}
function handleNewChat() { 
    currentChat = []; 
    clearChatDisplay(); 
}
function handleSaveClick(e) { 
    e.preventDefault();
    saveChat(); 
}

function setupEventListeners() {
    // List of elements that need event listeners
    const elementsToRefresh = [
        'sendButton', 
        'userInput', 
        'newChatButton', 
        'saveButton',
        'chatForm'
    ];

    // Refresh elements to remove duplicate listeners
    elementsToRefresh.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.replaceWith(el.cloneNode(true));
    });

    // Form submission handler
    document.getElementById('chatForm').addEventListener('submit', (e) => {
        e.preventDefault();
        sendMessage();
    });

    // Attach fresh event listeners
    document.getElementById('sendButton').addEventListener('click', handleSendClick);
    document.getElementById('userInput').addEventListener('keypress', handleKeyPress);
    document.getElementById('newChatButton').addEventListener('click', handleNewChat);
    document.getElementById('saveButton').addEventListener('click', handleSaveClick);
}

function displayMessage(message) {
    const chatlog = document.getElementById('chatlog');
    const messageDiv = document.createElement('div');
    
    messageDiv.className = `message ${message.sender}`;
    messageDiv.innerHTML = `
        <div class="message-header">
            <strong>${message.sender === 'user' ? 'You' : 'Medibot'}</strong>
        </div>
        <div class="message-content">${message.message}</div>
    `;

    chatlog.appendChild(messageDiv);
    chatlog.scrollTop = chatlog.scrollHeight;
}

function displayConversation(messages) {
    clearChatDisplay();
    messages.forEach(msg => displayMessage(msg));
}

function clearChatDisplay() {
    document.getElementById('chatlog').innerHTML = '';
}

async function loadChatHistory(suppressAlerts = false) {
    try {
        const response = await fetch('/get-chats');
        const chats = await response.json();
        
        const historyContainer = document.getElementById('chat-history');
        historyContainer.innerHTML = '';
        
        chats.forEach(chat => {
            const chatButton = document.createElement('button');
            chatButton.className = 'chat-history-btn';
            chatButton.innerHTML = `
                <span class="chat-date">${new Date(chat.timestamp).toLocaleDateString()}</span>
                <span class="chat-preview">${chat.messages[0]?.message.substring(0, 20)}...</span>
            `;
            
            chatButton.addEventListener('click', () => {
                currentChat = chat.messages;
                displayConversation(chat.messages);
            });
            
            historyContainer.appendChild(chatButton);
        });
    } catch (error) {
        console.error('Error loading chat history:', error);
        if (!suppressAlerts) alert('Failed to load chat history');
    }
}

async function saveChat() {
    if (currentChat.length === 0) {
        alert('No messages to save!');
        return;
    }

    try {
        const response = await fetch('/save-chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ messages: currentChat })
        });

        const data = await response.json();
        if (response.ok) {
            alert('Chat saved successfully!');
            currentChat = [];
            clearChatDisplay();
            loadChatHistory(true);
        } else {
            throw new Error(data.error || 'Failed to save chat');
        }
    } catch (error) {
        console.error('Save error:', error);
        alert(error.message);
    }
}

async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();

    if (!message) {
        alert('Please enter a message');
        return;
    }

    // Add user message
    const userMessage = {
        sender: 'user',
        message: message
    };
    currentChat.push(userMessage);
    displayMessage(userMessage);
    userInput.value = '';

    try {
        // Get bot response
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        const botMessage = {
            sender: 'bot',
            message: data.response
        };
        
        currentChat.push(botMessage);
        displayMessage(botMessage);
    } catch (error) {
        console.error('Error:', error);
        const errorMessage = {
            sender: 'bot',
            message: 'Sorry, I encountered an error. Please try again.'
        };
        currentChat.push(errorMessage);
        displayMessage(errorMessage);
    }
}