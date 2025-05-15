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
        if (!transactionsList) return;
        
        transactionsList.innerHTML = ''; // Limpiar la lista actual
        
        if (!transactions || transactions.length === 0) {
            transactionsList.innerHTML = `
                <div class="no-transactions">
                    <p>No hay transacciones recientes</p>
                </div>
            `;
            return;
        }

        transactions.forEach(transaction => {
            // ADAPTACIÓN: Usar estructura exacta del schema
            const type = transaction.tipo_transaccion.toLowerCase();
            
            // Determinar si el monto debe mostrarse como positivo o negativo
            let isPositive = false;
            
            if (type === 'deposito') {
                isPositive = true;
            } else if (type === 'retiro' || type === 'servicio') {
                isPositive = false;
            } else if (type === 'transferencia') {
                // Para transferencias, es positivo si es recibida y negativo si es enviada
                isPositive = transaction.descripcion?.includes('recibida') || false;
            }
            
            // Formatear el monto como moneda
            const amount = new Intl.NumberFormat('es-CO', {
                style: 'currency',
                currency: 'COP'
            }).format(Math.abs(parseFloat(transaction.monto)));

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
                    iconClass = transaction.descripcion?.includes('recibida') ? 
                        'fa-arrow-down' : 'fa-arrow-up';
                    break;
                case 'servicio':
                    iconClass = 'fa-file-invoice';
                    break;
                default:
                    iconClass = 'fa-exchange-alt';
            }

            // Formatear fecha
            const date = new Date(transaction.fecha_transaccion);
            const formattedDate = `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()} ${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`;

            // Crear elemento de transacción
            const transactionItem = document.createElement('div');
            transactionItem.className = 'transaction-item';
            transactionItem.innerHTML = `
                <div class="transaction-icon ${isPositive ? 'income' : 'expense'}">
                    <i class="fas ${iconClass}"></i>
                </div>
                <div class="transaction-info">
                    <div class="transaction-title">${transaction.descripcion || type}</div>
                    <div class="transaction-date">${formattedDate}</div>
                </div>
                <div class="transaction-amount ${isPositive ? 'income-text' : 'expense-text'}">
                    ${isPositive ? '+' : '-'} ${amount}
                </div>
            `;
            
            transactionsList.appendChild(transactionItem);
        });
        
    } catch (error) {
        console.error('Error al cargar transacciones:', error);
        const transactionsList = document.getElementById('recentTransactions');
        if (transactionsList) {
            transactionsList.innerHTML = `
                <div class="alert alert-danger">
                    Error al cargar transacciones recientes.
                </div>
            `;
        }
    }
}

// Cargar datos al iniciar
document.addEventListener('DOMContentLoaded', () => {
    refreshBalance();
    loadRecentTransactions();
    
    // Actualizar periódicamente
    setInterval(refreshBalance, 30000);  // Cada 30 segundos
    setInterval(loadRecentTransactions, 60000);  // Cada minuto
});