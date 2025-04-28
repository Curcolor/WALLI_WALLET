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

// Función para cargar transacciones recientes
async function loadRecentTransactions() {
    try {
        const response = await fetch('/api/recent-transactions');
        const transactions = await response.json();
        
        const transactionsList = document.getElementById('recentTransactions');
        transactionsList.innerHTML = ''; // Limpiar la lista actual
        
        if (transactions.length === 0) {
            transactionsList.innerHTML = `
                <div class="no-transactions">
                    <p>No hay transacciones recientes</p>
                </div>
            `;
            return;
        }

        transactions.forEach(transaction => {
            const type = transaction.tipo_transaccion.toLowerCase();
            // Determinar si el monto debe mostrarse como positivo o negativo
            let isPositive = false;
            
            if (type === 'deposito') {
                isPositive = true;
            } else if (type === 'retiro' || type === 'servicio') {
                isPositive = false;
            } else if (type === 'transferencia') {
                // Para transferencias, es positivo si es recibida y negativo si es enviada
                isPositive = transaction.descripcion.includes('recibida');
            }
            
            // Formatear el monto como moneda
            const amount = new Intl.NumberFormat('es-CO', {
                style: 'currency',
                currency: 'COP'
            }).format(Math.abs(transaction.monto));

            // Determinar el icono adecuado
            let iconClass = '';
            switch (type) {
                case 'deposito':
                    iconClass = 'fa-plus-circle';
                    break;
                case 'retiro':
                    iconClass = 'fa-minus-circle';
                    break;
                case 'transferencia':
                    iconClass = transaction.descripcion.includes('recibida') ? 
                        'fa-arrow-down' : 'fa-arrow-up';
                    break;
                case 'servicio':
                    iconClass = 'fa-file-invoice';
                    break;
                default:
                    iconClass = 'fa-exchange-alt';
            }

            const transactionHtml = `
                <div class="transaction-item">
                    <div class="transaction-icon ${type}">
                        <i class="fas ${iconClass}"></i>
                    </div>
                    <div class="transaction-details">
                        <h4 class="transaction-title">${transaction.descripcion}</h4>
                        <span class="transaction-date">${new Date(transaction.fecha_transaccion).toLocaleDateString('es-CO', {
                            day: 'numeric',
                            month: 'short',
                            year: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                        })}</span>
                    </div>
                    <div class="transaction-amount ${isPositive ? 'positive' : 'negative'}">
                        ${isPositive ? '+' : '-'} ${amount}
                    </div>
                </div>
            `;
            
            transactionsList.insertAdjacentHTML('beforeend', transactionHtml);
        });
    } catch (error) {
        console.error('Error al cargar las transacciones:', error);
        document.getElementById('recentTransactions').innerHTML = `
            <div class="error-message">
                <p>Error al cargar las transacciones</p>
            </div>
        `;
    }
}

// Cargar transacciones al iniciar
document.addEventListener('DOMContentLoaded', () => {
    loadRecentTransactions();
    // Actualizar cada 30 segundos
    setInterval(loadRecentTransactions, 30000);
});