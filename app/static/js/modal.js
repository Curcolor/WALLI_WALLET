function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
    }
}

function initializeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    
    const closeBtn = modal.querySelector('.modal-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => hideModal(modalId));
    }

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            hideModal(modalId);
        }
    });
}

// Inicializar todos los modales cuando se carga el documento
document.addEventListener('DOMContentLoaded', () => {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        initializeModal(modal.id);
    });
});

// Función para mostrar modal de éxito
function showSuccessModal(message, onClose = null) {
    // Crear el modal si no existe
    let successModal = document.getElementById('successModal');
    if (!successModal) {
        successModal = document.createElement('div');
        successModal.id = 'successModal';
        successModal.className = 'modal modal-success';
        successModal.innerHTML = `
            <div class="modal-content">
                <div class="modal-icon">
                    <i class="fas fa-check-circle"></i>
                </div>
                <h3>¡Éxito!</h3>
                <p id="successMessage"></p>
                <div class="modal-buttons">
                    <button id="successOk" class="modal-btn-confirm">Aceptar</button>
                </div>
            </div>
        `;
        document.body.appendChild(successModal);
    }

    successModal.querySelector('#successMessage').textContent = message;

    const okButton = successModal.querySelector('#successOk');
    okButton.onclick = () => {
        hideModal('successModal');
        if (onClose) onClose();
    };

    showModal('successModal');
}

// Función para mostrar modal de error
function showErrorModal(message, onClose = null) {
    let errorModal = document.getElementById('errorModal');
    if (!errorModal) {
        errorModal = document.createElement('div');
        errorModal.id = 'errorModal';
        errorModal.className = 'modal modal-error';
        errorModal.innerHTML = `
            <div class="modal-content">
                <div class="modal-icon">
                    <i class="fas fa-exclamation-circle"></i>
                </div>
                <h3>Error</h3>
                <p id="errorMessage"></p>
                <div class="modal-buttons">
                    <button id="errorOk" class="modal-btn-confirm">Aceptar</button>
                </div>
            </div>
        `;
        document.body.appendChild(errorModal);
    }

    errorModal.querySelector('#errorMessage').textContent = message;

    const okButton = errorModal.querySelector('#errorOk');
    okButton.onclick = () => {
        hideModal('errorModal');
        if (onClose) onClose();
    };

    showModal('errorModal');
} 