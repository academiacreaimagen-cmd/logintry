const API_URL = "/api"; // URL de la API

function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.form-content').forEach(f => f.classList.remove('active'));
    
    event.target.classList.add('active');
    document.getElementById(`${tab}-form`).classList.add('active');
}

// Toggle Password Visibility
document.getElementById('show-password').addEventListener('change', function() {
    const passwordInput = document.getElementById('login-password');
    passwordInput.type = this.checked ? 'text' : 'password';
});

// Login
document.getElementById('formLogin').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const mensajeDiv = document.getElementById('login-mensaje');
    
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            mensajeDiv.className = 'mensaje success';
            mensajeDiv.textContent = `✅ Bienvenido ${data.username}!`;
            mensajeDiv.style.display = 'block';
            
            // 🚀 Redirigir al dashboard después de 1 segundo
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1000);
            
        } else {
            mensajeDiv.className = 'mensaje error';
            mensajeDiv.textContent = `❌ ${data.detail}`;
            mensajeDiv.style.display = 'block';
        }
        
    } catch (error) {
        mensajeDiv.className = 'mensaje error';
        mensajeDiv.textContent = '❌ Error de conexión';
        mensajeDiv.style.display = 'block';
    }
});
