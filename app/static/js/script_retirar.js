document.addEventListener('DOMContentLoaded', function() {
    const withdrawForm = document.getElementById('withdrawForm');
    const withdrawAmount = document.getElementById('withdrawAmount');
    const confirmModal = document.getElementById('confirmModal');
    const confirmAmountSpan = document.getElementById('confirmAmount');
    const confirmWithdrawBtn = document.getElementById('confirmWithdraw');
    const cancelWithdrawBtn = document.getElementById('cancelWithdraw');
    const closeModal = document.querySelector('.close-modal');
    const balanceAmountSpan = document.getElementById('balanceAmount');

    // Manejar botones de montos rápidos
    document.querySelectorAll('.quick-amounts button').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            withdrawAmount.value = this.dataset.amount;
        });
    });

    // Mostrar modal de confirmación
    withdrawForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const monto = parseFloat(withdrawAmount.value);
        
        if (isNaN(monto) || monto < 1000) {
            alert('El monto mínimo de retiro es $1.000');
            return;
        }

        confirmAmountSpan.textContent = `$${monto.toLocaleString('es-CO')}`;
        confirmModal.style.display = 'block';
    });

    // Confirmar retiro
    confirmWithdrawBtn.addEventListener('click', async function() {
        try {
            const monto = parseFloat(withdrawAmount.value);
            console.log('Enviando solicitud de retiro:', monto); // Debug

            const response = await fetch('/api/retiro/retirar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ monto: monto })
            });

            const data = await response.json();
            console.log('Respuesta del servidor:', data); // Debug

            if (response.ok) {
                // Actualizar el saldo en la interfaz
                if (data.nuevo_saldo !== undefined) {
                    balanceAmountSpan.textContent = data.nuevo_saldo.toLocaleString('es-CO');
                }
                
                alert('Retiro realizado con éxito');
                confirmModal.style.display = 'none';
                withdrawForm.reset();
                
                // Redirigir al dashboard después de un retiro exitoso
                window.location.href = '/dashboard';
            } else {
                throw new Error(data.error || 'Error al procesar el retiro');
            }
        } catch (error) {
            console.error('Error durante el retiro:', error); // Debug
            alert(error.message);
        }
    });

    // Cerrar modal
    function cerrarModal() {
        confirmModal.style.display = 'none';
    }

    cancelWithdrawBtn.addEventListener('click', cerrarModal);
    closeModal.addEventListener('click', cerrarModal);

    // Cerrar modal si se hace clic fuera de él
    window.addEventListener('click', function(e) {
        if (e.target === confirmModal) {
            cerrarModal();
        }
    });
}); 