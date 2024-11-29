document.getElementById('paymentForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const referencia = document.querySelector('#paymentForm input[name="id_servicio"]').value;
    const monto = document.querySelector('#paymentForm input[type="number"]').value;
    
    // Obtener el saldo actual y convertirlo a número
    const saldoActual = parseFloat(document.getElementById('currentBalance').textContent.replace(/,/g, ''));
    
    // Verificar si hay saldo suficiente
    if (parseFloat(monto) > saldoActual) {
        alert('Saldo insuficiente para realizar el pago');
        return;
    }

    const data = {
        cuenta_id: 1, // Asegúrate de obtener el ID de cuenta correcto
        servicio_id: parseInt(referencia),
        monto: parseFloat(monto)
    };

    fetch('/api/pago-servicio/crear', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            alert('Pago realizado exitosamente');
            // Actualizar el saldo en la página
            const nuevoSaldo = saldoActual - parseFloat(monto);
            document.getElementById('currentBalance').textContent = 
                nuevoSaldo.toLocaleString('es-ES', {maximumFractionDigits: 0});
            // Limpiar el formulario
            event.target.reset();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al procesar el pago');
    });
});



