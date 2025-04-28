document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendMessage');

    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        messageDiv.innerHTML = `
            <i class="fas ${isUser ? 'fa-user' : 'fa-robot'}"></i>
            <div class="message-content">${message}</div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-message';
        typingDiv.innerHTML = `
            <i class="fas fa-robot"></i>
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return typingDiv;
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Agregar mensaje del usuario
        addMessage(message, true);
        userInput.value = '';

        // Agregar indicador de escritura
        const typingIndicator = addTypingIndicator();

        try {
            const response = await fetch('/chatbot/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            
            // Eliminar el indicador de escritura
            typingIndicator.remove();
            
            // Agregar la respuesta del bot
            addMessage(data.response);
        } catch (error) {
            // Eliminar el indicador de escritura
            typingIndicator.remove();
            addMessage('Lo siento, ha ocurrido un error al procesar tu mensaje.');
        }
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});