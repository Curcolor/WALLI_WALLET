// Función para validar formularios
function validarFormulario(formulario) {
    const campos = formulario.querySelectorAll('input[required]');
    let valido = true;

    campos.forEach(campo => {
        if (!campo.value) {
            campo.classList.add('error');
            valido = false;
        } else {
            campo.classList.remove('error');
        }
    });

    return valido;
}

// Manejador de eventos para formularios
document.addEventListener('DOMContentLoaded', () => {
    const formularios = document.querySelectorAll('form');
    
    formularios.forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!validarFormulario(form)) {
                e.preventDefault();
                alert('Por favor, complete todos los campos requeridos');
            }
        });
    });
}); 