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