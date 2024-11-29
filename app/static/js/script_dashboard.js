// Función para actualizar el saldo
async function refreshBalance() {
    try {
        const response = await fetch('/api/cuenta/saldo');
        const data = await response.json();
        
        if (response.ok) {
            const balanceElement = document.getElementById('balanceAmount');
            if (balanceElement) {
                balanceElement.textContent = data.saldo.toLocaleString('es-CO');
            }
        } else {
            console.error('Error al obtener el saldo:', data.error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Función para actualizar el saldo después de un retiro
function actualizarSaldoDespuesDeRetiro(nuevoSaldo) {
    const balanceElement = document.getElementById('balanceAmount');
    if (balanceElement) {
        balanceElement.textContent = nuevoSaldo.toLocaleString('es-CO');
    }
}

function cargarTransacciones() {
    fetch('/api/transferencia/historial', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        const transactionsList = document.getElementById('recentTransactions');
        transactionsList.innerHTML = ''; // Limpiar contenido existente

        if (data.transacciones.length === 0) {
            transactionsList.innerHTML = `
                <div class="no-transactions">
                    <p>No hay transacciones recientes</p>
                </div>
            `;
            return;
        }

        data.transacciones.forEach(trans => {
            const transactionEl = document.createElement('div');
            transactionEl.className = 'transaction-item';
            
            // Determinar el ícono según el canal
            let icono = '';
            switch (trans.canal) {
                case 'deposito':
                    icono = 'fa-plus-circle';
                    break;
                case 'retiro':
                    icono = 'fa-minus-circle';
                    break;
                case 'transferencia':
                    icono = 'fa-paper-plane';
                    break;
                default:
                    icono = 'fa-exchange-alt';
            }

            transactionEl.innerHTML = `
                <div class="transaction-icon">
                    <i class="fas ${icono}"></i>
                </div>
                <div class="transaction-details">
                    <div class="transaction-type">${trans.canal}</div>
                    <div class="transaction-date">${new Date(trans.fecha).toLocaleDateString('es-ES')}</div>
                </div>
                <div class="transaction-amount ${trans.canal === 'deposito' ? 'positive' : 'negative'}">
                    ${trans.canal === 'deposito' ? '+' : '-'} $${trans.monto.toLocaleString('es-ES')}
                </div>
                <div class="transaction-status ${trans.estado}">
                    ${trans.estado}
                </div>
            `;
            
            transactionsList.appendChild(transactionEl);
        });
    })
    .catch(error => {
        console.error('Error al cargar transacciones:', error);
    });
}

// Cargar transacciones cuando se carga la página
document.addEventListener('DOMContentLoaded', cargarTransacciones);
  