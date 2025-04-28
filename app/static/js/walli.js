async function sendMessage() {
    try {
        const userInput = document.getElementById('userIinput').value;
        if (!userInput.trim()) return;
        
        const chatDiv = document.getElementById('chatMessages');
        console.log('Enviando mensaje:', userInput);

        // Agrega el mensaje del usuario al chat
        chatDiv.innerHTML += `<div class="message user-message">
            <i class="fas fa-user"></i>
            <div class="message-content">
                ${userInput}
            </div>
        </div>`;

        // Limpia el campo de entrada
        document.getElementById('userIinput').value = '';

        // Muestra indicador de "escribiendo..."
        chatDiv.innerHTML += `<div class="message bot-message" id="loadingMessage">
            <i class="fas fa-robot"></i>
            <div class="message-content">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>`;
        chatDiv.scrollTop = chatDiv.scrollHeight;

        const response = await fetch('/api/walli/send', {
            method: 'POST',
            body: JSON.stringify({ message: userInput }),
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Eliminar el mensaje de carga
        const loadingMessage = document.getElementById('loadingMessage');
        if (loadingMessage) {
            loadingMessage.remove();
        }

        if (response.status === 401) {
            // Redirigir al login
            window.location.href = '/auth/login';
            return;
        }

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        const data = await response.json();
        
        // Agregar respuesta del bot
        chatDiv.innerHTML += `<div class="message bot-message">
            <i class="fas fa-robot"></i>
            <div class="message-content">
                ${data.response || data.error}
            </div>
        </div>`;
        chatDiv.scrollTop = chatDiv.scrollHeight;

    } catch (error) {
        console.error('Error:', error);
        const chatDiv = document.getElementById('chatMessages');
        chatDiv.innerHTML += `<div class="message bot-message error">
            <i class="fas fa-exclamation-triangle"></i>
            <div class="message-content">
                Lo siento, ha ocurrido un error al procesar tu mensaje.
            </div>
        </div>`;
    }
}

// Agregar eventos
document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('sendMessage');
    const inputField = document.getElementById('userIinput');

    sendButton.addEventListener('click', sendMessage);
    
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });
});