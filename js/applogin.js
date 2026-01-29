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
    const loginBox = document.querySelector('.container');
    const overlay = document.getElementById('loading-overlay');
    const waterFill = document.getElementById('water-fill');
    const welcomeText = document.getElementById('welcome-text');
    
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // 1. Ocultar el box de login
            loginBox.style.opacity = '0';
            loginBox.style.transform = 'scale(0.9)';
            
            setTimeout(() => {
                loginBox.style.display = 'none';
                
                // 2. Mostrar overlay de animación
                overlay.classList.add('active');
                
                // 3. Iniciar animación de "llenado de agua"
                setTimeout(() => {
                    waterFill.style.height = '100%';
                    
                    // 4. Mostrar Bienvenida
                    welcomeText.textContent = `¡Bienvenida ${data.username}!`;
                    welcomeText.classList.add('show');
                    
                    // 5. Redirigir después de que se llene
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 2500);
                }, 100);
            }, 500);
            
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
