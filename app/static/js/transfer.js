document.addEventListener('DOMContentLoaded', function() {
    const transferForm = document.getElementById('transferForm');
    const recipientAccount = document.getElementById('recipientAccount');
    const transferAmount = document.getElementById('transferAmount');
    const transferDescription = document.getElementById('transferDescription');
    const confirmRecipient = document.getElementById('confirmRecipient');
    const confirmAmount = document.getElementById('confirmAmount');
    const confirmTransferBtn = document.getElementById('confirmTransfer');
    const cancelTransferBtn = document.getElementById('cancelTransfer');

    // Mostrar modal de confirmación
    transferForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const monto = parseFloat(transferAmount.value);
        
        if (isNaN(monto) || monto < 1000) {
            alert('El monto mínimo de transferencia es $1.000');
            return;
        }

        confirmRecipient.textContent = recipientAccount.value;
        confirmAmount.textContent = `$${monto.toLocaleString('es-CO')}`;
        showModal('confirmModal');
    });

    // Confirmar transferencia
    confirmTransferBtn.addEventListener('click', async function() {
        try {
            const response = await fetch('/api/transferencia/transferir', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    cuenta_destino: recipientAccount.value,
                    monto: parseFloat(transferAmount.value),
                    descripcion: transferDescription.value
                })
            });

            const data = await response.json();

            if (response.ok) {
                showSuccessModal('Transferencia realizada con éxito', () => {
                    transferForm.reset();
                    window.location.href = '/dashboard';
                });
                hideModal('confirmModal');
            } else {
                showErrorModal('Error al procesar la transferencia');
            }
        } catch (error) {
            showErrorModal(error.message);
        }
    });

    // Cancelar transferencia
    cancelTransferBtn.addEventListener('click', () => hideModal('confirmModal'));
}); 