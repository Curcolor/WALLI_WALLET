document.addEventListener('DOMContentLoaded', function() {
    // Botones de cantidad rápida
    const quickAmountButtons = document.querySelectorAll('.quick-amounts button');
    const depositInput = document.getElementById('depositAmount');
    const depositForm = document.getElementById('depositForm');
    const modal = document.getElementById('confirmModal');
    const confirmAmount = document.getElementById('confirmAmount');
    const confirmButton = document.getElementById('confirmDeposit');
    const cancelButton = document.getElementById('cancelDeposit');

    // Manejar clicks en botones de cantidad rápida
    quickAmountButtons.forEach(button => {
        button.addEventListener('click', function() {
            depositInput.value = this.dataset.amount;
        });
    });

    // Manejar envío del formulario
    depositForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const amount = depositInput.value;
        if (amount < 1000) {
            alert('El monto mínimo de depósito es $1.000');
            return;
        }
        confirmAmount.textContent = `$${parseInt(amount).toLocaleString()}`;
        modal.style.display = 'flex';
    });

    // Manejar confirmación de depósito
    confirmButton.addEventListener('click', function() {
        const amount = depositInput.value;
        
        fetch('/api/deposito/crear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                monto: parseFloat(amount)
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.mensaje || 'Depósito realizado con éxito');
                
                // Actualizar saldo
                fetch('/api/cuenta/saldo')
                    .then(resp => resp.json())
                    .then(saldoData => {
                        if (saldoData.saldo !== undefined) {
                            const balanceElement = document.getElementById('currentBalance');
                            if (balanceElement) {
                                balanceElement.textContent = parseFloat(saldoData.saldo).toLocaleString('es-CO');
                            }
                        }
                    })
                    .catch(err => console.error('Error al actualizar saldo:', err));
                
                depositForm.reset();
            }
        })
        .catch(error => {
            alert('Error al procesar el depósito');
            console.error('Error:', error);
        })
        .finally(() => {
            modal.style.display = 'none';
        });
    });

    // Cerrar modal al cancelar
    cancelButton.addEventListener('click', function() {
        modal.style.display = 'none';
    });
});