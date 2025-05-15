document.addEventListener('DOMContentLoaded', function() {
    const transferForm = document.getElementById('transferForm');
    const recipientAccount = document.getElementById('recipientAccount');
    const transferAmount = document.getElementById('transferAmount');
    const transferDescription = document.getElementById('transferDescription');
    const confirmModal = document.getElementById('confirmModal');
    const confirmRecipient = document.getElementById('confirmRecipient');
    const confirmAmount = document.getElementById('confirmAmount');
    const confirmDescription = document.getElementById('confirmDescription');
    const confirmTransferBtn = document.getElementById('confirmTransfer');
    const cancelTransferBtn = document.getElementById('cancelTransfer');
    const closeModal = document.querySelector('.close-modal');

    // Mostrar modal de confirmación
    if (transferForm) {
        transferForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const monto = parseFloat(transferAmount.value);
            
            if (isNaN(monto) || monto < 1000) {
                alert('El monto mínimo de transferencia es $1.000');
                return;
            }
    
            confirmRecipient.textContent = recipientAccount.value;
            confirmAmount.textContent = `$${monto.toLocaleString('es-CO')}`;
            confirmDescription.textContent = transferDescription.value || '-';
            confirmModal.style.display = 'block';
        });
    }

    // Confirmar transferencia
    if (confirmTransferBtn) {
        confirmTransferBtn.addEventListener('click', async function() {
            try {
                const datosEnvio = {
                    cuenta_destino: recipientAccount.value,
                    monto: parseFloat(transferAmount.value),
                    descripcion: transferDescription.value || ''
                };
                
                console.log('Datos a enviar:', datosEnvio); // Debug
                
                const response = await fetch('/api/transferencia/transferir', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(datosEnvio)
                });
    
                const data = await response.json();
                
                console.log('Respuesta:', data); // Debug
    
                if (response.ok) {
                    // Actualizar el saldo en la interfaz
                    const balanceElement = document.getElementById('balanceAmount'); // Cambiado de 'currentBalance' a 'balanceAmount'
                    if (balanceElement && data.nuevo_saldo !== undefined) {
                        balanceElement.textContent = data.nuevo_saldo.toLocaleString('es-CO');
                    }
                    
                    alert('Transferencia realizada con éxito');
                    confirmModal.style.display = 'none';
                    transferForm.reset();
                    
                    // Redirigir al dashboard
                    window.location.href = '/dashboard';
                } else {
                    throw new Error(data.error || 'Error al procesar la transferencia');
                }
            } catch (error) {
                console.error('Error completo:', error); // Debug
                alert(error.message);
            }
        });
    }

    // Cerrar modal
    function cerrarModal() {
        confirmModal.style.display = 'none';
    }

    if (cancelTransferBtn) cancelTransferBtn.addEventListener('click', cerrarModal);
    if (closeModal) closeModal.addEventListener('click', cerrarModal);

    // Cerrar modal si se hace clic fuera de él
    window.addEventListener('click', function(e) {
        if (e.target === confirmModal) {
            cerrarModal();
        }
    });
});