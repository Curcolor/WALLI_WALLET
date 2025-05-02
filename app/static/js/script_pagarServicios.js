document.addEventListener('DOMContentLoaded', function() {
    // Cargar lista de servicios al inicio
    cargarServicios();
    
    const paymentForm = document.getElementById('paymentForm');
    
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // ADAPTACIÓN: Actualizar para usar select de servicios
            const servicioId = document.getElementById('serviceSelect').value;
            const monto = document.getElementById('paymentAmount').value;
            const referencia = document.getElementById('referenceNumber')?.value || '';
            
            // Obtener el saldo actual y convertirlo a número
            const saldoActual = parseFloat(document.getElementById('currentBalance')?.textContent.replace(/,/g, '') || 0);
            
            // Verificaciones básicas
            if (!servicioId || servicioId === "0") {
                alert('Seleccione un servicio');
                return;
            }
            
            if (!monto || isNaN(monto) || parseFloat(monto) <= 0) {
                alert('Ingrese un monto válido');
                return;
            }
            
            // Verificar si hay saldo suficiente
            if (parseFloat(monto) > saldoActual) {
                alert('Saldo insuficiente para realizar el pago');
                return;
            }
        
            const data = {
                servicio_id: parseInt(servicioId),
                monto: parseFloat(monto),
                referencia: referencia
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
                    alert(data.mensaje || 'Pago realizado exitosamente');
                    
                    // Actualizar el saldo en la página
                    if (data.nuevo_saldo !== undefined) {
                        document.getElementById('currentBalance').textContent = 
                            parseFloat(data.nuevo_saldo).toLocaleString('es-ES');
                    } else {
                        actualizarSaldo();
                    }
                    
                    // Limpiar el formulario
                    event.target.reset();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al procesar el pago');
            });
        });
    }
    
    // Función para cargar servicios disponibles
    function cargarServicios() {
        fetch('/api/pago-servicio/servicios')
            .then(response => response.json())
            .then(data => {
                const serviceSelect = document.getElementById('serviceSelect');
                if (!serviceSelect) return;
                
                // Limpiar opciones existentes
                serviceSelect.innerHTML = '<option value="0">Seleccione un servicio</option>';
                
                // ADAPTACIÓN: Usar la estructura con "servicios"
                const servicios = data.servicios || [];
                
                if (servicios.length > 0) {
                    servicios.forEach(servicio => {
                        const option = document.createElement('option');
                        option.value = servicio.id_servicio;
                        option.textContent = `${servicio.nombre_servicio} - ${servicio.empresa || 'N/A'}`;
                        serviceSelect.appendChild(option);
                    });
                } else {
                    const option = document.createElement('option');
                    option.textContent = 'No hay servicios disponibles';
                    option.disabled = true;
                    serviceSelect.appendChild(option);
                }
            })
            .catch(error => {
                console.error('Error al cargar servicios:', error);
                const serviceSelect = document.getElementById('serviceSelect');
                if (serviceSelect) {
                    serviceSelect.innerHTML = '<option value="0">Error al cargar servicios</option>';
                }
            });
    }
    
    // Función para actualizar el saldo
    function actualizarSaldo() {
        fetch('/api/cuenta/saldo')
            .then(response => response.json())
            .then(data => {
                if (data.saldo !== undefined) {
                    const balanceElement = document.getElementById('currentBalance');
                    if (balanceElement) {
                        balanceElement.textContent = parseFloat(data.saldo).toLocaleString('es-ES');
                    }
                }
            })
            .catch(error => {
                console.error('Error al actualizar saldo:', error);
            });
    }
});



